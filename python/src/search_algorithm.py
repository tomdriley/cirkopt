from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, Sequence, TypeVar, Callable, Optional
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
Simulator = Callable[[Sequence[Candidate]], SimulationResult]


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


class SearchAlgorithm(Generic[Candidate, SimulationResult]):
    __metaclass__ = ABCMeta

    _candidate_generator: CandidateGenerator[Candidate]
    _cost_function: Optional[CostFunction]
    _simulate: Optional[Simulator]
    _candidates: Sequence[Candidate]
    _iteration: int
    _simulation_result: SimulationResult
    _cost_map: CostMap

    def search(self) -> Candidate:
        info("Generating initial population.")
        self._candidates = self._candidate_generator.get_initial_population()

        self._iteration = 0
        while True:
            info(f"Starting iteration {self._iteration}")

            self._simulation_result = self.simulate(self._candidates)
            self._cost_map = self.cost_function(
                self._candidates, self._simulation_result
            )

            self._iteration += 1
            if self._should_stop():
                break

            self._candidates = self._candidate_generator.get_next_population(
                self._candidates, self._cost_map
            )

        info("Selecting best candidate.")
        best_candidate_name, _ = min(self._cost_map.items(), key=lambda item: item[1])
        return single(lambda c: c.key() == best_candidate_name, self._candidates)

    @abstractmethod
    def _should_stop(self) -> bool:
        pass

    def _post_simulation(self):
        pass

    def simulate(self, candidates: Sequence[Candidate]) -> SimulationResult:
        assert self._simulate is not None
        return self._simulate(candidates)

    def cost_function(
        self, candidates: Sequence[Candidate], results: SimulationResult
    ) -> CostMap:
        assert self._cost_function is not None
        return self._cost_function(candidates, results)
