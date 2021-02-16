from dataclasses import dataclass
from typing import Any, Dict, Callable, Sequence
from unittest import TestCase

from src.search_algorithm import CandidateClass, CandidateGenerator, \
    CostFunction, CostMap, SearchAlgorithm


@dataclass(frozen=True)
class TestCandidate(CandidateClass):
    ckey: str = ""
    cost: float = 0.0

    def key(self) -> str:
        return self.ckey


class TestCandidateGenerator(CandidateGenerator[TestCandidate]):
    dict_equal_assert: Callable[[Dict, Dict], None]

    def __init__(self, dict_equal_assert: Callable[[Dict, Dict], None]):
        self.dict_equal_assert = dict_equal_assert

    # pylint: disable=no-self-use
    def get_initial_population(self) -> Sequence[TestCandidate]:
        return tuple(TestCandidate(f"cand_{i}", float(i)) for i in range(5))

    def get_next_population(
            self,
            current_candidates: Sequence[TestCandidate],
            cost_map: CostMap
    ) -> Sequence[TestCandidate]:
        expected_cost_map = {candidate.ckey: candidate.cost for candidate in current_candidates}
        self.dict_equal_assert(cost_map, expected_cost_map)
        return current_candidates


class TestCostFunction(CostFunction[TestCandidate, Any]):
    # pylint: disable=no-self-use,unused-argument
    def calculate(self, candidates: Sequence[TestCandidate], simulation_result: Any) -> CostMap:
        return {candidate.ckey: candidate.cost for candidate in candidates}


class TestSearchAlgorithm(SearchAlgorithm[TestCandidate, Any]):
    num_times_simulate_called: int
    iteration: int

    def __init__(
            self,
            cost_function: TestCostFunction,
            candidate_generator: TestCandidateGenerator
    ):
        self.cost_function = cost_function
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
        def dict_equal_assert(first: Dict, second: Dict):
            self.assertDictEqual(first, second)

        candidate_generator = TestCandidateGenerator(dict_equal_assert)
        cost_function = TestCostFunction()
        search_algorithm = TestSearchAlgorithm(cost_function, candidate_generator)

        result = search_algorithm.search()

        self.assertEqual(5, search_algorithm.iteration)
        self.assertEqual(5, search_algorithm.num_times_simulate_called)
        self.assertEqual(result.ckey, "cand_0")
        self.assertEqual(result.cost, 0.0)
