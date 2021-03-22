from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Generic, Sequence, TypeVar, Callable, Optional, Tuple
from logging import info

from src.utils import single

SimulationResult = TypeVar("SimulationResult")
CostMap = Dict[str, float]


class CandidateClass:
    __metaclass__ = ABCMeta

    @abstractmethod
    def key(self) -> str:
        pass


Candidate = TypeVar("Candidate", bound=CandidateClass)

CostFunction = Callable[[Sequence[Candidate], SimulationResult], CostMap]
Simulator = Callable[[Sequence[Candidate], int], SimulationResult]


class CandidateGenerator(Generic[Candidate]):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_initial_population(self) -> Sequence[Candidate]:
        pass

    @abstractmethod
    def get_next_population(
        self, current_candidates: Sequence[Candidate], cost_map: CostMap
    ) -> Sequence[Candidate]:
        pass


@dataclass
class CandidateCache(Generic[Candidate]):
    _size: int
    _cache: Dict[int, float] = field(default_factory=dict, init=False)
    _hits: int = field(default=0, init=False)
    _misses: int = field(default=0, init=False)

    def __post_init__(self):
        assert self._size > 0

    def get(self, candidates: Sequence[Candidate]) -> Tuple[CostMap, Sequence[Candidate]]:
        """Returns costs for cached candidates and misses"""
        # Get cached costs by hash on candidate
        cached_cost_map: CostMap = {
            c.key(): self._cache[hash(c)]
            for c in candidates
            if hash(c) in self._cache
        }
        self._hits += len(cached_cost_map)

        # Identify the cache misses
        uncached_candidates = tuple(filter(function=lambda c: c.key() not in cached_cost_map, iterable=candidates))
        self._misses += len(uncached_candidates)
        return cached_cost_map, uncached_candidates

    def update(self, candidates: Sequence[Candidate], cost_map: CostMap):
        # Make one big cache with existing and new entries, deduplicate using dict
        new_cache_entries = {hash(c): cost_map[c.key()] for c in candidates}
        combined_cache = {**self._cache, **new_cache_entries}

        # Only keep the N lowest costs
        all_candidates_and_costs = list(combined_cache.items())
        all_candidates_and_costs.sort(key=lambda hash_and_cost: hash_and_cost[1])
        self._cache = dict(all_candidates_and_costs[:self._size])

    def hits(self) -> int:
        return self._hits

    def misses(self) -> int:
        return self._misses


class SearchAlgorithm(Generic[Candidate, SimulationResult]):
    __metaclass__ = ABCMeta

    _candidate_generator: CandidateGenerator[Candidate]
    _cost_function: Optional[CostFunction]
    _simulate: Optional[Simulator]
    _candidates: Sequence[Candidate]
    _iteration: int
    _simulation_result: SimulationResult
    _cost_map: CostMap
    _best_candidate: Optional[Tuple[Candidate, float]] = None
    _candidate_cache: Optional[CandidateCache[Candidate]] = None  # Override to enable caching best candidates

    def search(self) -> Candidate:
        info("Generating initial population.")
        self._candidates = self._candidate_generator.get_initial_population()

        self._iteration = 0
        while len(self._candidates) > 0:
            info(f"Starting iteration {self._iteration}")

            self._simulate_and_compute_costs()
            self._post_simulation()

            # Update current best
            _, current_best_cost = self._best_candidate or (None, float("inf"))
            iteration_best_key, iteration_best_cost = min(self._cost_map.items(), key=lambda item: item[1])
            if iteration_best_cost < current_best_cost:
                info(f"New best cost found! Updating from cost of {current_best_cost} to {iteration_best_cost}")
                iteration_best_candidate = single(lambda c: c.key() == iteration_best_key, self._candidates)
                self._best_candidate = (iteration_best_candidate, iteration_best_cost)

            self._iteration += 1
            if self._should_stop():
                break

            self._candidates = self._candidate_generator.get_next_population(
                self._candidates, self._cost_map
            )

        info("Selecting best candidate.")
        assert self._best_candidate is not None
        return self._best_candidate[0]

    def _simulate_and_compute_costs(self):
        # If caching not enabled, proceed normally
        if self._candidate_cache is None:
            self._simulation_result = self.simulate(self._candidates, self._iteration)
            self._cost_map = self.cost_function(self._candidates, self._simulation_result)
            return

        # Get what we can from the cache, then simulate and calc cost for cache misses
        cached_cost_map, uncached_candidates = self._candidate_cache.get(self._candidates)
        self._simulation_result = self.simulate(uncached_candidates, self._iteration)
        uncached_cost_map = self.cost_function(uncached_candidates, self._simulation_result)

        self._candidate_cache.update(uncached_candidates, uncached_cost_map)

        self._cost_map = {**cached_cost_map, **uncached_cost_map}

    @abstractmethod
    def _should_stop(self) -> bool:
        pass

    def _post_simulation(self):
        pass

    def simulate(self, candidates: Sequence[Candidate], iteration: int) -> SimulationResult:
        assert self._simulate is not None
        return self._simulate(candidates, iteration)

    def cost_function(self, candidates: Sequence[Candidate], results: SimulationResult) -> CostMap:
        assert self._cost_function is not None
        return self._cost_function(candidates, results)
