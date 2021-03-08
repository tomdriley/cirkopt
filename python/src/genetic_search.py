from dataclasses import dataclass
from itertools import chain
from math import ceil, log10
from typing import Callable, Optional, Sequence, Tuple

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


def _normalize(netlist: Netlist, precision: float) -> Tuple[int, ...]:
    """Returns the netlist's fixed point widths, fixed point lengths and fingers in a 1d tuple"""
    widths = (quantize(w, precision) for w in netlist.device_widths)
    lengths = (quantize(l, precision) for l in netlist.device_lengths)
    fingers = iter(netlist.device_fingers)
    return tuple(chain(widths, lengths, fingers))


def _denormalize(
        normalized_netlist: np.ndarray,
        precision: float
) -> Tuple[Tuple[float, ...], Tuple[float, ...], Tuple[int, ...]]:
    """Returns the normalized netlist's floating point widths, floating point lengths and fingers"""
    ndevices = normalized_netlist.shape[0]
    return (
        tuple(scale(w, precision) for w in normalized_netlist[:ndevices]),
        tuple(scale(l, precision) for l in normalized_netlist[ndevices:-ndevices]),
        tuple(normalized_netlist[-ndevices:])
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
    _min_width: int  # fixed point
    _max_width: int  # fixed point
    _min_length: int  # fixed point
    _max_length: int  # fixed point
    _precision: float
    _fingers_values: Sequence[int]

    # Netlist
    _reference_netlist: Netlist
    _number_of_devices: int  # How many devices the generated netlists have, cached for convenience
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
            precision: float,
            fingers_values: Sequence[int],
            reference_netlist: Netlist,
            netlist_persister: Optional[Callable[[Netlist], None]],
            seed: Optional[int] = None
    ):
        # pylint: disable=too-many-locals
        return cls(
            _num_individuals=num_individuals,
            _elitism=elitism,
            _n_points=npoints,
            _alpha=alpha,
            _pmutation=pmutation,
            _mutation_std_deviation=mutation_std_deviation,
            _min_width=quantize(min_width, precision, Rounding.HALF_UP),  # TODO: look into rounding up
            _max_width=quantize(max_width, precision, Rounding.HALF_UP),  # TODO: look into rounding down
            _min_length=quantize(min_length, precision, Rounding.HALF_UP),  # TODO: look into rounding up
            _max_length=quantize(max_length, precision, Rounding.HALF_UP),  # TODO: look into rounding down
            _precision=precision,
            _fingers_values=fingers_values,
            _reference_netlist=reference_netlist,
            _number_of_devices=len(reference_netlist.device_widths),
            _id_num_digits=ceil(log10(num_individuals)),
            _netlist_persister=netlist_persister,
            _rng=(default_rng(seed=seed) if seed is not None else default_rng())
        )

    def get_initial_population(self) -> Sequence[Netlist]:
        """
        Generate N (self._num_individuals) netlists where each netlist has random device widths, lengths and fingers.
        The randomized widths, lengths and fingers follow a normal distribution and satisfy the constraints given in
        class initializer.

        :return: a sequence of randomly generated netlists which have been persisted to disk.
        """
        def rand_netlist(idx: int) -> Netlist:
            # Generate fixed point widths and lengths
            widths = self._rng.integers(self._min_width, self._max_width, self._number_of_devices, endpoint=True)
            lengths = self._rng.integers(self._min_length, self._max_length, self._number_of_devices, endpoint=True)
            # randomly choose finger values from provided values
            fingers = self._rng.choice(self._fingers_values, self._number_of_devices)

            return self._reference_netlist.mutate(
                cell_name=self._get_netlist_name(idx),
                device_widths=tuple(scale(w, self._precision) for w in widths),  # convert from fixed point
                device_lengths=tuple(scale(l, self._precision) for l in lengths),
                device_fingers=fingers
            )

        netlists = [rand_netlist(idx) for idx in range(self._num_individuals)]
        self._persist_netlists(netlists)
        return netlists

    def get_next_population(self, current_candidates: Sequence[Netlist], cost_map: CostMap) -> Sequence[Netlist]:
        # pylint: disable=too-many-locals
        # Ensure same order as current_candidates
        costs = np.asarray([cost_map[n.key()] for n in current_candidates], dtype=np.float32)

        # TODO: Make mating pool size configurable maybe?
        # Candidates with lower cost have higher probability of being a parent
        parenting_probabilities = 1 - (costs / costs.sum())

        # Two NxM arrays where N is number of individuals and M is 3 * number of devices per individual
        mating_pool = np.asarray([_normalize(n, self._precision) for n in current_candidates], dtype=np.uint16)
        offspring = np.zeros((self._num_individuals, self._number_of_devices * 3), dtype=np.uint16)

        def maybe_add_child_to_offspring(child_to_add: np.ndarray, child_idx: int) -> bool:
            """Adds child if it doesn't already exist by some fluke. Also checks bounds. Returns if child was added"""
            # Don't add if it would be out of bounds
            if child_idx >= offspring.shape[0]:
                return False

            for idx, child in enumerate(offspring):
                if idx > child_idx:
                    break  # break early since from here on out it'll all be zeros

                if child_to_add == child:
                    return False  # if child already exists in offspring, don't add
            # Child not found in offspring, so it can be added
            offspring[child_idx] = child_to_add
            return True

        assert mating_pool.shape == offspring.shape

        num_children = 0
        while num_children < self._num_individuals:
            # draw 2 parents from mating pool
            parent_indices = np.random.choice(
                a=mating_pool.shape[0],
                size=2,
                replace=False,
                p=parenting_probabilities
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
            lowest_cost_parent = costs.argmin()
            random_offspring = self._rng.choice(range(self._num_individuals), 1)
            offspring[random_offspring] = mating_pool[lowest_cost_parent]

        netlists = []
        for idx, normalized_netlist in enumerate(offspring):
            assert normalized_netlist.any(), f"Offspring[{idx}] contained only zeros"

            widths, lengths, fingers = _denormalize(normalized_netlist, self._precision)
            netlists.append(self._reference_netlist.mutate(self._get_netlist_name(idx), widths, lengths, fingers))

        self._persist_netlists(netlists)
        return netlists

    def _n_point_arithmetic_crossover(
            self,
            parent_a: np.ndarray,
            parent_b: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        assert len(parent_a) == len(parent_b)

        # Select n random indices to crossover
        points = self._rng.choice(range(len(parent_a)), self._n_points)

        mix_mask = np.zeros_like(parent_a, dtype=np.bool8)
        mix_mask[points] |= True
        keep_mask = np.invert(mix_mask)

        a = self._alpha
        # Perform crossover
        # for k in points: child_a[k] = alpha * parent_a[k] + (1-alpha) * parent_b[k]
        child_a = (parent_a * keep_mask) + (a * mix_mask * parent_a) + ((1-a) * mix_mask * parent_b)
        child_b = (parent_b * keep_mask) + ((1-a) * mix_mask * parent_a) + (a * mix_mask * parent_b)

        return child_a.round().astype(np.uint16), child_b.round().astype(np.uint16)

    def _gaussian_mutation(self, individual: np.ndarray) -> np.ndarray:
        """Apply additive gaussian noise to each device parameter with a probability of self._pmutation"""
        p = self._pmutation
        mutation_mask = self._rng.choice([0, 1], len(individual), p=[1-p, p]).asType(np.bool8)
        mutations = self._rng.normal(0, 1, len(individual))
        return (individual + mutations * mutation_mask).round().astype(np.uint16)

    def _get_netlist_name(self, idx: int) -> str:
        return self._reference_netlist.cell_name + "_" + str(idx).zfill(self._id_num_digits)

    def _persist_netlists(self, netlists: Sequence[Netlist]):
        assert self._netlist_persister is not None
        for netlist in netlists:
            self._netlist_persister(netlist)


class GeneticSearch(SearchAlgorithm):
    _max_iterations: int

    def __init__(
        self,
        candidate_generator: GeneticCandidateGenerator,
        cost_function: CostFunction,
        max_iterations: int
    ):
        self._candidate_generator = candidate_generator
        self._cost_function = cost_function
        self._simulate = liberate_simulator
        self._max_iterations = max_iterations

    def _should_stop(self) -> bool:
        return self._iteration >= self._max_iterations
