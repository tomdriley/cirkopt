from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, Sequence, TypeVar

from src.utils import single

SimulationResult = TypeVar('SimulationResult')
CostMap = Dict[str, float]


class CandidateClass:
    __metaclass__ = ABCMeta

    @abstractmethod
    def key(self) -> str:
        pass


Candidate = TypeVar('Candidate', bound=CandidateClass)


class CostFunction(Generic[Candidate, SimulationResult]):
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate(
            self,
            candidates: Sequence[Candidate],
            simulation_result: SimulationResult
    ) -> CostMap:
        pass


class CandidateGenerator(Generic[Candidate]):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_initial_population(self) -> Sequence[Candidate]:
        pass

    @abstractmethod
    def get_next_population(
            self,
            current_candidates: Sequence[Candidate],
            cost_map: CostMap
    ) -> Sequence[Candidate]:
        pass


class SearchAlgorithm(Generic[Candidate, SimulationResult]):
    __metaclass__ = ABCMeta

    cost_function: CostFunction
    candidate_generator: CandidateGenerator[Candidate]

    def search(self) -> Candidate:
        candidates = self.candidate_generator.get_initial_population()

        iteration = 0
        while True:
            simulation_result = self._simulate(candidates)
            cost_map = self.cost_function.calculate(candidates, simulation_result)

            iteration += 1
            if self._should_stop(iteration):
                break

            candidates = self.candidate_generator.get_next_population(candidates, cost_map)

        best_candidate_name, _ = min(cost_map.items(), key=lambda item: item[1])
        return single(lambda c: c.key() == best_candidate_name, candidates)

    @abstractmethod
    def _should_stop(self, iteration: int) -> bool:
        pass

    @abstractmethod
    def _simulate(self, candidates: Sequence[Candidate]) -> SimulationResult:
        pass
