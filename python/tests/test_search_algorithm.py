from dataclasses import dataclass
from typing import Any, Sequence
from unittest import TestCase

from src.search_algorithm import (
    CandidateClass,
    CandidateGenerator,
    CostFunction,
    CostMap,
    SearchAlgorithm,
)


@dataclass(frozen=True)
class TestCandidate(CandidateClass):
    ckey: str = ""
    cost: float = 0.0

    def key(self) -> str:
        return self.ckey


class TestCandidateGenerator(CandidateGenerator[TestCandidate]):
    # pylint: disable=no-self-use
    def get_initial_population(self) -> Sequence[TestCandidate]:
        return tuple(TestCandidate(f"cand_{i}", float(i)) for i in range(5))

    def get_next_population(
        self, current_candidates: Sequence[TestCandidate], cost_map: CostMap
    ) -> Sequence[TestCandidate]:
        expected_cost_map = {
            candidate.ckey: candidate.cost for candidate in current_candidates
        }
        assert cost_map == expected_cost_map
        return current_candidates


def test_cost_function(
    candidates: Sequence[TestCandidate], simulation_result: Any
) -> CostMap:
    return {candidate.ckey: candidate.cost for candidate in candidates}


class TestSearchAlgorithm(SearchAlgorithm[TestCandidate, Any]):
    num_times_simulate_called: int
    iteration: int

    def __init__(
        self,
        candidate_generator: TestCandidateGenerator,
        cost_function=test_cost_function,
    ):
        self._cost_function = cost_function
        self.candidate_generator = candidate_generator
        self.num_times_simulate_called = 0
        self.iteration = 0

    def _should_stop(self, iteration: int):
        self.iteration = iteration
        return iteration == 5

    # pylint: disable=unused-argument
    def _simulate(self, candidates: Sequence[TestCandidate]) -> Any:
        self.num_times_simulate_called += 1


class TestSearchAlgorithms(TestCase):
    def test_search_algorithm_classes(self):
        candidate_generator = TestCandidateGenerator()
        search_algorithm = TestSearchAlgorithm(candidate_generator)

        result = search_algorithm.search()

        self.assertEqual(5, search_algorithm.iteration)
        self.assertEqual(5, search_algorithm.num_times_simulate_called)
        self.assertEqual(result.ckey, "cand_0")
        self.assertEqual(result.cost, 0.0)
