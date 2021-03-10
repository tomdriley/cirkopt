from dataclasses import dataclass
from enum import Enum
from itertools import chain
from math import ceil, log10
from typing import Callable, List, Optional, Sequence, Set, Tuple
from logging import debug

from numpy.random import default_rng
import numpy as np

from src.quantize import quantize, scale, Rounding
from src.liberate import liberate_simulator
from src.liberty_parser import LibertyResult
from src.netlist import Netlist
from src.search_algorithm import (
    CandidateGenerator,
    CostMap,
    SearchAlgorithm,
)

CostFunction = Callable[[Sequence[Netlist], LibertyResult], CostMap]


class Param(Enum):
    WIDTH = 1
    LENGTH = 2
    FINGERS = 3

@dataclass(frozen=True)
class Bounds:
    min_width: int
    max_width: int
    min_length: int
    max_length: int
    min_fingers: int
    max_fingers: int


def _normalize(netlist: Netlist, precision: str) -> Tuple[int, ...]:
    """Returns the netlist's fixed point widths, fixed point lengths and fingers in a 1d tuple"""
    widths = (quantize(w, precision) for w in netlist.device_widths)
    lengths = (quantize(l, precision) for l in netlist.device_lengths)
    fingers = iter(netlist.device_fingers)
    return tuple(chain(widths, lengths, fingers))


def _denormalize(
    normalized_netlist: np.ndarray, precision: str, b: Bounds
) -> Tuple[Tuple[float, ...], Tuple[float, ...], Tuple[int, ...]]:
    """Returns the normalized netlist's floating point widths, floating point lengths and fingers"""
    ndevices = normalized_netlist.shape[0] // 3
    return (
        tuple(
            scale(w, precision)
            for w in normalized_netlist[:ndevices].clip(b.min_width, b.max_width)
        ),
        tuple(
            scale(l, precision)
            for l in normalized_netlist[ndevices:-ndevices].clip(
                b.min_length, b.max_length
            )
        ),
        tuple(normalized_netlist[-ndevices:].clip(b.min_fingers, b.max_fingers)),
    )


# None of this data should be mutable
@dataclass(frozen=True)
class GeneticCandidateGenerator(CandidateGenerator[Netlist]):
    # pylint: disable=too-many-instance-attributes
    # Population params
    _num_individuals: int  # Number of candidates in a population
    _elitism: bool  # Whether the best candidate should be included in the next generation
    _n_points: int  # How many points to perform arithmetic crossover on two parents
    _alpha: float  # Alpha for arithmetic crossover
    _pmutation: float  # Probability a mutation will occur to a device parameter
    _mutation_std_deviation: float  # Standard deviation of additive gaussian noise mutation

    # Search space params
    _bounds: Bounds
    _precision: str

    # Netlist
    _reference_netlist: Netlist
    _number_of_devices: int  # How many devices the generated netlists have, cached for convenience
    _search_params: Set[Param]  # Which params the search can very
    _variable_indices: List[int]  # Which indices in an individual can be varied
    _id_num_digits: int  # How many digits the _id should have, cached for convenience
    _netlist_persister: Optional[Callable[[Netlist], None]]

    _rng: np.random.Generator

    @classmethod
    def create(
        cls,
        num_individuals: int,
        elitism: bool,
        npoints: int,
        alpha: float,
        pmutation: float,
        mutation_std_deviation: float,
        min_width: float,
        max_width: float,
        min_length: float,
        max_length: float,
        min_fingers: int,
        max_fingers: int,
        precision: str,
        reference_netlist: Netlist,
        netlist_persister: Optional[Callable[[Netlist], None]],
        seed: Optional[int] = None,
    ):
        # pylint: disable=too-many-locals)
        search_params = set()
        if min_width != max_width:
            search_params.add(Param.WIDTH)
        if min_length != max_length:
            search_params.add(Param.LENGTH)
        if min_fingers != max_fingers:
            search_params.add(Param.FINGERS)

        number_of_devices = len(reference_netlist.device_widths)
        indices = [
            idx
            for param in search_params
            for idx in range((param.value - 1) * number_of_devices, param.value * number_of_devices)
        ]

        if npoints > len(indices):
            raise ValueError("npoints should be less than or equal to the number of number of devices per "
                             "netlist * number of params the algorithm can vary. "
                             "For example if the algorithm can very length and width for an inverter, nppoints <= 4"
                             "(2 devices * 2 params).")

        # pylint: disable=too-many-locals
        return cls(
            _num_individuals=num_individuals,
            _elitism=elitism,
            _n_points=npoints,
            _alpha=alpha,
            _pmutation=pmutation,
            _mutation_std_deviation=mutation_std_deviation,
            _bounds=Bounds(
                min_width=quantize(
                    min_width, precision, Rounding.TIE_EVEN
                ),  # TODO: look into rounding up
                max_width=quantize(
                    max_width, precision, Rounding.TIE_EVEN
                ),  # TODO: look into rounding down
                min_length=quantize(
                    min_length, precision, Rounding.TIE_EVEN
                ),  # TODO: look into rounding up
                max_length=quantize(
                    max_length, precision, Rounding.TIE_EVEN
                ),  # TODO: look into rounding down
                min_fingers=min_fingers,
                max_fingers=max_fingers,
            ),
            _precision=precision,
            _reference_netlist=reference_netlist,
            _number_of_devices=number_of_devices,
            _search_params=search_params,
            _variable_indices=indices,
            _id_num_digits=ceil(log10(num_individuals)),
            _netlist_persister=netlist_persister,
            _rng=(default_rng(seed=seed) if seed is not None else default_rng()),
        )

    def get_initial_population(self) -> Sequence[Netlist]:
        """
        Generate N (self._num_individuals) netlists where each netlist has random device widths, lengths and fingers.
        The randomized widths, lengths and fingers follow a normal distribution and satisfy the constraints given in
        class initializer.

        :return: a sequence of randomly generated netlists which have been persisted to disk.
        """
        b = self._bounds
        n = self._number_of_devices

        def rand_netlist(idx: int) -> Netlist:
            # Generate fixed point widths if we can vary them
            if Param.WIDTH in self._search_params:
                widths = self._rng.integers(b.min_width, b.max_width, n, endpoint=True, dtype=np.uint16)
            else:
                widths = b.min_width * np.ones(n, dtype=np.uint16)

            # Generate fixed point lengths if we can vary them
            if Param.LENGTH in self._search_params:
                lengths = self._rng.integers(b.min_length, b.max_length, n, endpoint=True, dtype=np.uint16)
            else:
                lengths = b.min_length * np.ones(n, dtype=np.uint16)

            if Param.FINGERS in self._search_params:
                fingers = self._rng.integers(b.min_fingers, b.max_fingers, n, endpoint=True, dtype=np.uint16)
            else:
                fingers = b.min_fingers * np.ones(n, dtype=np.uint16)

            return self._reference_netlist.mutate(
                cell_name=self._get_netlist_name(idx),
                device_widths=tuple(scale(w, self._precision) for w in widths),
                device_lengths=tuple(scale(l, self._precision) for l in lengths),
                device_fingers=tuple(fingers),
            )

        netlists = [rand_netlist(idx) for idx in range(self._num_individuals)]
        self._persist_netlists(netlists)
        return netlists

    def get_next_population(
        self, current_candidates: Sequence[Netlist], cost_map: CostMap
    ) -> Sequence[Netlist]:
        # pylint: disable=too-many-locals
        # Fitness is inverse of cost, ensure same order as current_candidates
        fitness = np.asarray(
            [1.0 / cost_map[n.key()] for n in current_candidates], dtype=np.float32
        )

        # TODO: Make mating pool size configurable maybe?
        # Candidates with lower cost have higher probability of being a parent
        parenting_probabilities = fitness / fitness.sum()

        # Two NxM arrays where N is number of individuals and M is 3 * number of devices per individual
        mating_pool = np.asarray(
            [_normalize(n, self._precision) for n in current_candidates],
            dtype=np.uint16,
        )
        offspring = np.zeros(
            (self._num_individuals, self._number_of_devices * 3), dtype=np.uint16
        )

        def maybe_add_child_to_offspring(
            child_to_add: np.ndarray, child_idx: int
        ) -> bool:
            """Adds child if it doesn't already exist by some fluke. Also checks bounds. Returns if child was added"""
            # Don't add if it would be out of bounds
            if child_idx >= offspring.shape[0]:
                return False

            for idx, child in enumerate(offspring):
                if idx > child_idx:
                    break  # break early since from here on out it'll all be zeros

                if (child_to_add == child).all():
                    return False  # if child already exists in offspring, don't add
            # Child not found in offspring, so it can be added
            offspring[child_idx] = child_to_add
            return True

        assert mating_pool.shape == offspring.shape

        num_children = 0
        while num_children < self._num_individuals:
            # draw 2 parents from mating pool
            parent_indices = np.random.choice(
                a=mating_pool.shape[0], size=2, replace=False, p=parenting_probabilities
            )

            # Perform crossover
            parent_a, parent_b = mating_pool[parent_indices]
            child_a, child_b = self._n_point_arithmetic_crossover(parent_a, parent_b)

            # Perform mutation
            child_a = self._gaussian_mutation(child_a)
            child_b = self._gaussian_mutation(child_b)

            if maybe_add_child_to_offspring(child_a, num_children):
                num_children += 1
            if maybe_add_child_to_offspring(child_b, num_children):
                num_children += 1

        # elitism
        if self._elitism:
            lowest_cost_parent = fitness.argmax()
            offspring[lowest_cost_parent] = mating_pool[lowest_cost_parent]

            # perform a local search on best individual as well, don't replace the one we just added
            valid_indices = [idx for idx in range(self._num_individuals) if idx != lowest_cost_parent]
            rand_child = self._rng.choice(valid_indices, 1)
            offspring[rand_child] = self._gaussian_mutation(mating_pool[lowest_cost_parent])

        netlists = []
        for idx, normalized_netlist in enumerate(offspring):
            assert normalized_netlist.any(), f"Offspring[{idx}] contained only zeros"

            widths, lengths, fingers = _denormalize(
                normalized_netlist, self._precision, self._bounds
            )
            netlists.append(
                self._reference_netlist.mutate(
                    self._get_netlist_name(idx), widths, lengths, fingers
                )
            )

        self._persist_netlists(netlists)
        return netlists

    def _n_point_arithmetic_crossover(
        self,
        parent_a: np.ndarray,
        parent_b: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        assert len(parent_a) == len(parent_b)

        indices = self._variable_indices
        if len(indices) == self._n_points:
            points = indices
        else:
            # Select n random indices to crossover
            points = self._rng.choice(indices, self._n_points)

        mix_mask = np.zeros_like(parent_a, dtype=np.bool8)
        mix_mask[points] |= True
        keep_mask = np.invert(mix_mask)

        a = self._alpha
        # Perform crossover
        # for k in points: child_a[k] = a * parent_a[k] + (1-a) * parent_b[k]
        child_a = (
            (parent_a * keep_mask)
            + (a * mix_mask * parent_a)
            + ((1 - a) * mix_mask * parent_b)
        )
        child_b = (
            (parent_b * keep_mask)
            + ((1 - a) * mix_mask * parent_a)
            + (a * mix_mask * parent_b)
        )

        return child_a.round().astype(np.uint16), child_b.round().astype(np.uint16)

    def _gaussian_mutation(self, individual: np.ndarray) -> np.ndarray:
        """Apply additive gaussian noise to each device parameter with a probability of self._pmutation"""
        def round_based_on_sign(v: np.float32) -> np.int32:
            if v > 0:
                return np.ceil(v)
            if v < 0:
                return np.floor(v)
            return np.int32(0)

        vectorized_round_based_on_sign = np.vectorize(round_based_on_sign, otypes=[np.int16])

        # get the indices we can modify based on self._search_params
        indices = self._variable_indices
        n = len(indices)

        # Select which device parameters to be mutated each with a probability of p
        p = self._pmutation
        mutation_mask = np.zeros(len(individual), dtype=np.bool8)
        mutation_mask[indices] = self._rng.choice([0, 1], n, p=[1-p, p]).astype(np.bool8)

        # Sample mutations from normal distribution, then use a symmetric rounding where mutations below zero are
        # rounded down and mutations above zero are rounded up
        # This ensures that if a device parameter is chosen to be mutates it is at least changed by +/- 1
        mutations = self._rng.normal(0, self._mutation_std_deviation, len(individual))
        rounded_mutations = vectorized_round_based_on_sign(mutations)

        # Returns device params can't be negative, clip blow zero and cast to uint
        return np.max(individual + rounded_mutations * mutation_mask, 0).astype(np.uint16)

    def _get_netlist_name(self, idx: int) -> str:
        return (
            self._reference_netlist.cell_name
            + "_"
            + str(idx).zfill(self._id_num_digits)
        )

    def _persist_netlists(self, netlists: Sequence[Netlist]):
        assert self._netlist_persister is not None
        for netlist in netlists:
            self._netlist_persister(netlist)


class GeneticSearch(SearchAlgorithm[Netlist, LibertyResult]):
    _max_iterations: int
    min_cost_per_iteration: List[float]

    def __init__(
        self,
        candidate_generator: GeneticCandidateGenerator,
        cost_function: CostFunction,
        max_iterations: int,
    ):
        self._candidate_generator = candidate_generator
        self._cost_function = cost_function
        self._simulate = liberate_simulator
        self._max_iterations = max_iterations
        self.min_cost_per_iteration = [0] * max_iterations

    def _should_stop(self) -> bool:
        return self._iteration >= self._max_iterations

    def _post_simulation(self):
        min_cost_per_iteration = min(self._cost_map.values())
        debug(f"minimum cost of interation {self._iteration}: {min_cost_per_iteration}")
        self.min_cost_per_iteration[self._iteration] = min_cost_per_iteration
