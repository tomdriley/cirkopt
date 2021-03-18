from dataclasses import dataclass
from itertools import chain
from math import ceil, log10
from typing import List, Optional, Sequence, Set, Tuple, Type
from logging import debug
from decimal import Decimal

from numpy.random import default_rng
import numpy as np

from src.circuit_search_common import Param, Range
from src.quantize import quantize
from src.liberty_parser import LibertyResult
from src.netlist import Netlist
from src.search_algorithm import (
    CandidateGenerator,
    CostMap,
    SearchAlgorithm,
    Simulator,
    CostFunction,
)


@dataclass(frozen=True)
class Bounds:
    widths: Sequence[Decimal]
    step_width: Decimal
    lengths: Sequence[Decimal]
    step_length: Decimal
    fingers: Sequence[int]
    step_fingers: int

    @classmethod
    def from_range(
        cls: Type['Bounds'],
        width_range: Range[Decimal],
        length_range: Range[Decimal],
        fingers_range: Range[int]
    ) -> 'Bounds':
        return cls(
            widths=list(width_range),
            step_width=width_range.step_size,
            lengths=list(length_range),
            step_length=length_range.step_size,
            fingers=list(fingers_range),
            step_fingers=fingers_range.step_size
        )


def _normalize(netlist: Netlist, b: Bounds) -> Tuple[int, ...]:
    """Returns the netlist's fixed point widths, fixed point lengths and fingers in a 1d tuple"""
    widths = (quantize(Decimal(w), b.step_width, b.widths[0]) for w in netlist.device_widths)
    lengths = (quantize(Decimal(l), b.step_length, b.lengths[0]) for l in netlist.device_lengths)
    fingers = (max(f - b.fingers[0], 0) // b.step_fingers for f in netlist.device_fingers)
    return tuple(chain(widths, lengths, fingers))


def _denormalize(
    normalized_netlist: np.ndarray, b: Bounds
) -> Tuple[Tuple[float, ...], Tuple[float, ...], Tuple[int, ...]]:
    """Returns the normalized netlist's floating point widths, floating point lengths and fingers"""
    ndevices = normalized_netlist.shape[0] // 3

    # Clip to ensure values are valid
    quantized_widths = normalized_netlist[:ndevices].clip(0, len(b.widths) - 1)
    quantized_lengths = normalized_netlist[ndevices:-ndevices].clip(0, len(b.lengths) - 1)
    quantized_fingers = normalized_netlist[-ndevices:].clip(0, len(b.fingers) - 1)
    return (
        tuple(float(b.widths[w]) for w in quantized_widths),
        tuple(float(b.lengths[l]) for l in quantized_lengths),
        tuple(b.fingers[f] for f in quantized_fingers),
    )


# None of this data should be mutable
@dataclass(frozen=True)
class GeneticCandidateGenerator(CandidateGenerator[Netlist]):
    # pylint: disable=too-many-instance-attributes
    # Population params
    _num_individuals: int  # Number of candidates in a population
    _elitism: bool  # Whether the best candidate should be included in the next generation
    _npoints: int  # How many points to perform arithmetic crossover on two parents
    _alpha: float  # Alpha for arithmetic crossover
    _pmutation: float  # Probability a mutation will occur to a device parameter
    _mutation_std_deviation: float  # Standard deviation of additive gaussian noise mutation

    # Search space params
    _bounds: Bounds

    # Netlist
    _reference_netlist: Netlist
    _ndevices: int  # How many devices the generated netlists have, cached for convenience
    _search_params: Set[Param]  # Which params the search can vary
    _variable_indices: List[int]  # Which indices in an individual can be varied
    _id_num_digits: int  # How many digits the _id should have, cached for convenience

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
        width_range: Range[Decimal],
        length_range: Range[Decimal],
        fingers_range: Range[int],
        reference_netlist: Netlist,
        seed: Optional[int] = None,
    ):
        # pylint: disable=too-many-locals)
        bounds = Bounds.from_range(width_range, length_range, fingers_range)
        search_params = []
        if len(bounds.widths) > 1:
            search_params.append(Param.WIDTH)
        if len(bounds.lengths) > 1:
            search_params.append(Param.LENGTH)
        if len(bounds.fingers) > 1:
            search_params.append(Param.FINGERS)
        debug(f"Search params: {search_params}")

        ndevices = len(reference_netlist.device_widths)
        variable_indices = [
            idx
            for param in search_params
            for idx in range((param.value - 1) * ndevices, param.value * ndevices)
        ]

        if npoints > len(variable_indices):
            raise ValueError(
                "npoints should be less than or equal to the number of number of devices per "
                "netlist * number of params the algorithm can vary. "
                "For example if the algorithm can very length and width for an inverter, nppoints <= 4"
                "(2 devices * 2 params)."
            )

        # pylint: disable=too-many-locals
        return cls(
            _num_individuals=num_individuals,
            _elitism=elitism,
            _npoints=npoints,
            _alpha=alpha,
            _pmutation=pmutation,
            _mutation_std_deviation=mutation_std_deviation,
            _bounds=bounds,
            _reference_netlist=reference_netlist,
            _ndevices=ndevices,
            _search_params=set(search_params),
            _variable_indices=variable_indices,
            _id_num_digits=ceil(log10(num_individuals)),
            _rng=(default_rng(seed=seed) if seed is not None else default_rng()),
        )

    def get_initial_population(self) -> Sequence[Netlist]:
        """
        Generate N (self._num_individuals) netlists where each netlist has random device widths, lengths and fingers.
        The randomized widths, lengths and fingers follow a normal distribution and satisfy the constraints given in
        class initializer.

        :return: a sequence of randomly generated netlists
        """
        b = self._bounds
        n = self._ndevices

        def rand_netlist(idx: int) -> Netlist:
            # Generate fixed point widths if we can vary them
            if Param.WIDTH in self._search_params:
                widths = self._rng.integers(0, len(b.widths), n, dtype=np.uint64)
            else:
                widths = np.zeros(n, dtype=np.uint64)

            # Generate fixed point lengths if we can vary them
            if Param.LENGTH in self._search_params:
                lengths = self._rng.integers(0, len(b.lengths), n, dtype=np.uint64)
            else:
                lengths = np.zeros(n, dtype=np.uint64)

            if Param.FINGERS in self._search_params:
                fingers = self._rng.integers(0, len(b.fingers), n, dtype=np.uint64)
            else:
                fingers = np.zeros(n, dtype=np.uint64)

            return self._reference_netlist.clone(
                cell_name=self._get_netlist_name(idx),
                device_widths=tuple(float(b.widths[w]) for w in widths),
                device_lengths=tuple(float(b.lengths[l]) for l in lengths),
                device_fingers=tuple(b.fingers[f] for f in fingers),
            )

        return [rand_netlist(idx) for idx in range(self._num_individuals)]

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
        mating_pool = np.asarray([_normalize(n, self._bounds) for n in current_candidates], dtype=np.uint64)
        offspring = np.zeros((self._num_individuals, self._ndevices * 3), dtype=np.uint64)

        def maybe_add_child_to_offspring(child_to_add: np.ndarray, child_idx: int) -> bool:
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
            valid_indices = [
                idx for idx in range(self._num_individuals) if idx != lowest_cost_parent
            ]
            rand_child = self._rng.choice(valid_indices, 1)
            offspring[rand_child] = self._gaussian_mutation(mating_pool[lowest_cost_parent])

        netlists = []
        for idx, normalized_netlist in enumerate(offspring):
            assert normalized_netlist.any(), f"Offspring[{idx}] contained only zeros"

            widths, lengths, fingers = _denormalize(normalized_netlist, self._bounds)
            netlists.append(
                self._reference_netlist.clone(self._get_netlist_name(idx), widths, lengths, fingers)
            )

        return netlists

    def _n_point_arithmetic_crossover(
        self,
        parent_a: np.ndarray,
        parent_b: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        assert len(parent_a) == len(parent_b)

        indices = self._variable_indices
        if len(indices) == self._npoints:
            points = indices
        else:
            # Select n random indices to crossover
            points = self._rng.choice(indices, self._npoints)

        mix_mask = np.zeros_like(parent_a, dtype=np.bool8)
        mix_mask[points] |= True
        keep_mask = np.invert(mix_mask)

        a = self._alpha
        # Perform crossover
        # for k in points: child_a[k] = a * parent_a[k] + (1-a) * parent_b[k]
        child_a = (
            (parent_a * keep_mask) + (a * mix_mask * parent_a) + ((1 - a) * mix_mask * parent_b)
        )
        child_b = (
            (parent_b * keep_mask) + ((1 - a) * mix_mask * parent_a) + (a * mix_mask * parent_b)
        )

        return child_a.round().astype(np.uint64), child_b.round().astype(np.uint64)

    def _gaussian_mutation(self, individual: np.ndarray) -> np.ndarray:
        """Apply additive gaussian noise to each device parameter with a probability of self._pmutation"""

        def round_based_on_sign(v: np.float32) -> np.int64:
            if v > 0:
                return np.ceil(v)
            if v < 0:
                return np.floor(v)
            return np.int64(0)

        vectorized_round_based_on_sign = np.vectorize(round_based_on_sign, otypes=[np.int64])

        # get the indices we can modify based on self._search_params
        indices = self._variable_indices
        n = len(indices)

        # Select which device parameters to be mutated each with a probability of p
        p = self._pmutation
        mutation_mask = np.zeros(len(individual), dtype=np.bool8)
        mutation_mask[indices] = self._rng.choice([0, 1], n, p=[1 - p, p]).astype(np.bool8)

        # Sample mutations from normal distribution, then use a symmetric rounding where mutations below zero are
        # rounded down and mutations above zero are rounded up
        # This ensures that if a device parameter is chosen to be mutated it is at least changed by +/- 1
        mutations = self._rng.normal(0, self._mutation_std_deviation, len(individual))
        rounded_mutations = vectorized_round_based_on_sign(mutations)

        # Returns device params can't be negative, clip below zero and cast to uint
        return np.maximum(individual + rounded_mutations * mutation_mask, 0).astype(np.uint64)

    def _get_netlist_name(self, idx: int) -> str:
        return self._reference_netlist.cell_name + "_" + str(idx).zfill(self._id_num_digits)


class GeneticSearch(SearchAlgorithm[Netlist, LibertyResult]):
    _max_iterations: int
    min_cost_per_iteration: List[float]

    def __init__(
        self,
        simulator: Simulator,
        candidate_generator: GeneticCandidateGenerator,
        cost_function: CostFunction,
        max_iterations: int,
    ):
        self._candidate_generator = candidate_generator
        self._cost_function = cost_function
        self._simulate = simulator
        self._max_iterations = max_iterations
        self.min_cost_per_iteration = [0] * max_iterations

    def _should_stop(self) -> bool:
        return self._iteration >= self._max_iterations

    def _post_simulation(self):
        self.min_cost_per_iteration[self._iteration] = min(self._cost_map.values())
