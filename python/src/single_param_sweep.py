from enum import Enum
from typing import Any, Callable, Sequence, Union

from src.file_io import IFile
from src.liberate import run_liberate
from src.liberty_parser import Group, LibertyParser
from src.netlist import Netlist
from src.search_algorithm import (
    CandidateGenerator,
    CostFunction,
    CostMap,
    SearchAlgorithm,
)


class Param(Enum):
    WIDTH = 1
    LENGTH = 2
    FINGERS = 3

    def __str__(self):
        if self == Param.WIDTH:
            return "Width"
        elif self == Param.LENGTH:
            return "Length"
        else:
            return "Fingers"


class ParamSweepCandidateGenerator(CandidateGenerator[Netlist]):
    """
    Given N values for a Param, generate N netlists where each device in each
    netlist is given one value for the param.
    For example, given Param.WIDTH and values (260e-9, 310e-9) two netlists
    would be generated, one with all device widths set to 260e-9 and the other 310e-9
    """

    candidates: Sequence[Netlist]

    def __init__(
        self,
        reference_netlist: Netlist,
        netlist_persister: Callable[[Netlist], None],
        param: Param,
        values: Sequence[Union[float, int]],
    ):
        base_name = reference_netlist.cell_name

        def new_netlist(version: int, val: Union[float, int]):
            widths = reference_netlist.device_widths
            lengths = reference_netlist.device_lengths
            fingers = reference_netlist.device_fingers
            cell_name = base_name + f"_{version:02}"

            if param == Param.WIDTH:
                widths = tuple(float(val) for _ in range(len(widths)))
            elif param == Param.LENGTH:
                lengths = tuple(float(val) for _ in range(len(lengths)))
            else:
                fingers = tuple(int(val) for _ in range(len(lengths)))
            return reference_netlist.mutate(cell_name, widths, lengths, fingers)

        self.candidates = tuple(
            new_netlist(idx, value) for idx, value in enumerate(values)
        )
        for candidate in self.candidates:
            netlist_persister(candidate)

    # pylint: disable=no-self-use
    def get_initial_population(self) -> Sequence[Netlist]:
        return self.candidates

    def get_next_population(
        self, current_candidates: Sequence[Netlist], cost_map: CostMap
    ) -> Sequence[Netlist]:
        return self.candidates


class NoopCostFunction(CostFunction[Netlist, Any]):
    """Noop cost function"""

    # pylint: disable=no-self-use,unused-argument
    def calculate(
        self, candidates: Sequence[Netlist], simulation_result: Any
    ) -> CostMap:
        return {candidate.key(): 0.0 for candidate in candidates}


class SingleParamSweep(SearchAlgorithm[Netlist, Group]):
    """Does 1 simulation that simulates all candidates provided by candidate_generator."""

    liberty_parser: LibertyParser
    sim_file: IFile

    def __init__(
        self,
        cost_function: NoopCostFunction,
        candidate_generator: ParamSweepCandidateGenerator,
        liberty_parser: LibertyParser,
        sim_file: IFile,
    ):
        self.cost_function = cost_function
        self.candidate_generator = candidate_generator
        self.liberty_parser = liberty_parser
        self.sim_file = sim_file

    def _should_stop(self, iteration: int):
        return iteration == 1

    # pylint: disable=unused-argument
    def _simulate(self, candidates: Sequence[Netlist]) -> Group:
        cell_names = tuple(netlist.cell_name for netlist in candidates)
        # TODO: paramaterize other args
        run_liberate(cell_names=cell_names)
        return self.liberty_parser.parse(self.sim_file)
