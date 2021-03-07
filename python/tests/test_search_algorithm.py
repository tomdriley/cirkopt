from dataclasses import dataclass
from typing import Sequence, Mapping, Dict
from unittest import TestCase

from src.search_algorithm import (
    CandidateClass,
    CandidateGenerator,
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
    def __init__(self, initial_population: Sequence[float]):
        self._initial_population_values = initial_population

    def get_initial_population(self) -> Sequence[TestCandidate]:
        return tuple(
            TestCandidate(f"cand_{i}", val)
            for i, val in enumerate(self._initial_population_values)
        )

    def get_next_population(
        self, current_candidates: Sequence[TestCandidate], cost_map: CostMap
    ) -> Sequence[TestCandidate]:
        return tuple(
            candidate
            for candidate in current_candidates
            if cost_map[candidate.key()] == 0.0
        )


def test_cost_function(
    candidates: Sequence[TestCandidate],
    simulation_result: Mapping[str, float],
) -> CostMap:
    return {
        candidate.key(): simulation_result[candidate.key()] for candidate in candidates
    }


def test_simulator(candidates: Sequence[TestCandidate]) -> Dict[str, float]:
    result = {candidate.key(): 0.0 for candidate in candidates}
    if candidates[0].value < candidates[1].value:
        result[candidates[0].key()] = 1.0
    else:
        result[candidates[1].key()] = 1.0
    return result


class TestSearchAlgorithm(SearchAlgorithm[TestCandidate, Dict[str, float]]):
    num_times_simulate_called: int
    iteration: int

    def __init__(
        self,
        candidate_generator: TestCandidateGenerator,
        cost_function=test_cost_function,
        simulate=test_simulator,
    ):
        self._candidate_generator = candidate_generator
        self._cost_function = cost_function
        self._simulate = simulate

    def _should_stop(self):
        return len(self._candidates) == 2

    def get_candidates(self):
        return self._candidates

    def get_simulation_result(self):
        return self._simulation_result

    def get_cost_map(self):
        return self._cost_map

    def get_iteration(self):
        return self._iteration


class TestSearchAlgorithms(TestCase):
    def test_search_algorithm_classes(self):
        values = (3, 7.6, 5, 1.1)
        candidate_generator = TestCandidateGenerator(values)
        search_algorithm = TestSearchAlgorithm(candidate_generator)

        result = search_algorithm.search()

        self.assertEqual(search_algorithm.get_iteration(), 3)
        self.assertEqual(result.name, "cand_1")
        self.assertEqual(result.value, 7.6)
        self.assertEqual(
            search_algorithm.get_candidates(),
            (TestCandidate("cand_1", 7.6), TestCandidate("cand_3", 1.1)),
        )
        self.assertEqual(
            search_algorithm.get_simulation_result(), {"cand_1": 0.0, "cand_3": 1.0}
        )
        self.assertEqual(
            search_algorithm.get_cost_map(), search_algorithm.get_simulation_result()
        )
