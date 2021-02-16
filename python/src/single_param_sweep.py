from typing import Any, Callable, Sequence

from src.file_io import IFile
from src.liberate import run_liberate
from src.liberty_parser import Group, LibertyParser
from src.netlist import Netlist
from src.search_algorithm import CandidateGenerator, CostFunction, CostMap, SearchAlgorithm


class ParamSweepCandidateGenerator(CandidateGenerator[Netlist]):
    candidates: Sequence[Netlist]

    def __init__(self, reference_netlist: Netlist, netlist_persister: Callable[[Netlist], None]):
        # TODO: generate a bunch of new netlist with new values
        pass

    # pylint: disable=no-self-use
    def get_initial_population(self) -> Sequence[Netlist]:
        return self.candidates

    def get_next_population(
            self,
            current_candidates: Sequence[Netlist],
            cost_map: CostMap
    ) -> Sequence[Netlist]:
        return self.candidates


class NoopCostFunction(CostFunction[Netlist, Any]):
    # pylint: disable=no-self-use,unused-argument
    def calculate(self, candidates: Sequence[Netlist], simulation_result: Any) -> CostMap:
        return {candidate.key(): 0.0 for candidate in candidates}


class SingleParamSweep(SearchAlgorithm[Netlist, Group]):
    liberty_parser: LibertyParser
    sim_file: IFile

    def __init__(
            self,
            cost_function: NoopCostFunction,
            candidate_generator: ParamSweepCandidateGenerator,
            liberty_parser: LibertyParser,
            sim_file: IFile
    ):
        self.cost_function = cost_function
        self.candidate_generator = candidate_generator
        self.liberty_parser = liberty_parser
        self.sim_file = sim_file

    def _should_stop(self, iteration: int):
        return iteration == 1

    # pylint: disable=unused-argument
    def _simulate(self, candidates: Sequence[Netlist]) -> Group:
        run_liberate()
        return self.liberty_parser.parse(self.sim_file)
