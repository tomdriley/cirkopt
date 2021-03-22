from dataclasses import dataclass
from typing import Sequence, Dict, Optional
from unittest import TestCase

from src.search_algorithm import (
    CandidateClass,
    CandidateGenerator,
    CandidateCache,
    CostMap,
    SearchAlgorithm,
)


@dataclass(frozen=True)
class TestCandidate(CandidateClass):
    name: str = ""
    value: float = 0.0

    def key(self) -> str:
        return self.name


class TestCandidateGenerator(CandidateGenerator[TestCandidate]):

    def get_initial_population(self) -> Sequence[TestCandidate]:
        return tuple(TestCandidate(f"cand_{i}", float(i)) for i in [2, 4, 6, 8, 10])

    def get_next_population(
        self, current_candidates: Sequence[TestCandidate], cost_map: CostMap
    ) -> Sequence[TestCandidate]:
        return tuple(TestCandidate(f"cand_{i}", float(i)) for i in [1, 2, 3, 5, 7])


def test_cost_function(
    candidates: Sequence[TestCandidate],
    simulation_result: Dict[str, float],
) -> CostMap:
    return {c.key(): simulation_result[c.key()] for c in candidates}


def test_simulator(candidates: Sequence[TestCandidate], iteration: int) -> Dict[str, float]:
    # pylint: disable=unused-argument
    return {c.key(): c.value for c in candidates}


class TestSearchAlgorithm(SearchAlgorithm[TestCandidate, Dict[str, float]]):

    def __init__(
        self,
        candidate_generator: TestCandidateGenerator,
        cost_function=test_cost_function,
        simulate=test_simulator,
        cache: Optional[CandidateCache[TestCandidate]] = None
    ):
        self._candidate_generator = candidate_generator
        self._cost_function = cost_function
        self._simulate = simulate
        self._candidate_cache = cache

    def _should_stop(self):
        return self._iteration == 2


class TestSearchAlgorithms(TestCase):
    # pylint: disable=protected-access

    def test_search_algorithm_classes(self):
        candidate_generator = TestCandidateGenerator()
        search_algorithm = TestSearchAlgorithm(candidate_generator)
        result = search_algorithm.search()

        second_candidates = candidate_generator.get_next_population(list(), dict())

        self.assertEqual(search_algorithm._iteration, 2)
        self.assertEqual(result.name, "cand_1")
        self.assertEqual(result.value, 1.0)
        self.assertSequenceEqual(search_algorithm._candidates, second_candidates)
        self.assertDictEqual(
            search_algorithm._simulation_result,
            {c.key(): c.value for c in second_candidates}
        )
        self.assertDictEqual(
            search_algorithm._cost_map,
            {c.key(): c.value for c in second_candidates}
        )

    def test_search_algorithm_classes_with_caching(self):
        candidate_generator = TestCandidateGenerator()
        search_algorithm = TestSearchAlgorithm(candidate_generator, cache=CandidateCache(4))
        result = search_algorithm.search()

        second_candidates = list(candidate_generator.get_next_population(list(), dict()))

        self.assertEqual(search_algorithm._iteration, 2)
        self.assertEqual(result.name, "cand_1")
        self.assertEqual(result.value, 1.0)
        self.assertSequenceEqual(search_algorithm._candidates,second_candidates)
        self.assertDictEqual(
            search_algorithm._simulation_result,
            {c.key(): c.value for c in second_candidates[:1] + second_candidates[2:]}  # second candidate was cached
        )
        self.assertDictEqual(
            search_algorithm._cost_map,
            {c.key(): c.value for c in second_candidates}
        )

        cache = search_algorithm._candidate_cache
        self.assertEqual(cache._size, 4)
        self.assertEqual(cache.hits(), 1)
        self.assertEqual(cache.misses(), 9)
        expected_cache = {hash(TestCandidate(f"cand_{i}", float(i))): float(i) for i in range(1, 5)}
        self.assertDictEqual(cache._cache, expected_cache)

    def test_candidate_cache(self):
        candidate_generator = TestCandidateGenerator()
        candidates = list(candidate_generator.get_initial_population())
        next_candidates = list(candidate_generator.get_next_population(candidates, dict()))

        # Test cache initialization
        cache: CandidateCache[TestCandidate] = CandidateCache(8)
        self.assertEqual(cache.misses(), 0)
        self.assertEqual(cache.hits(), 0)
        self.assertEqual(cache._size, 8)

        # Test empty cache
        empty_cost_map, uncached_candidates = cache.get(candidates)
        self.assertEqual(len(empty_cost_map), 0)
        self.assertSequenceEqual(candidates, uncached_candidates)
        self.assertEqual(cache.misses(), 5)
        self.assertEqual(cache.hits(), 0)

        # Test partial update to cache
        cost_map = {c.key(): c.value for c in candidates}
        cache.update(candidates, cost_map)
        self.assertDictEqual({hash(c): c.value for c in candidates}, cache._cache)

        # Test 100% cache hit
        cached_cost_map, uncached_candidates = cache.get(candidates)
        self.assertEqual(len(uncached_candidates), 0)
        self.assertDictEqual(cached_cost_map, cost_map)
        self.assertEqual(cache.misses(), 5)
        self.assertEqual(cache.hits(), 5)

        # Test partial cache miss on partially filled cache, second candidate already in cache
        partial_cost_map, uncached_candidates = cache.get(next_candidates)
        self.assertEqual(len(partial_cost_map), 1)
        self.assertSequenceEqual(next_candidates[:1] + next_candidates[2:], uncached_candidates)
        self.assertEqual(cache.misses(), 9)
        self.assertEqual(cache.hits(), 6)

        next_cost_map = {c.key(): c.value for c in next_candidates}
        cache.update(next_candidates, next_cost_map)  # deduplicate second candidate already in cache
        expected_cache = {hash(c): c.value for c in candidates[:4] + next_candidates}  # Cand with val 10 doesnt make it
        self.assertDictEqual(expected_cache, cache._cache)

        # Test 8 hits and 1 misses on fully filled cache
        cached_cost_map, uncached_candidates = cache.get(candidates + next_candidates)
        self.assertEqual(len(uncached_candidates), 1)
        self.assertSequenceEqual(candidates[4:], uncached_candidates)
        expected_cost_map = {c.key(): c.value for c in candidates[:4] + next_candidates}
        self.assertDictEqual(cached_cost_map, expected_cost_map)
        self.assertEqual(cache.misses(), 10)
        self.assertEqual(cache.hits(), 14)
