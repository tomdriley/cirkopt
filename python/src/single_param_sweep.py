from typing import Sequence, Union

from src.circuit_search_common import Param
from src.liberty_parser import LibertyResult
from src.netlist import Netlist
from src.search_algorithm import (
    CandidateGenerator,
    CostMap,
    SearchAlgorithm,
    Simulator,
)
from src.netlist_cost_functions import noop_cost_function


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
                fingers = tuple(int(val) for _ in range(len(fingers)))
            return reference_netlist.clone(cell_name, widths, lengths, fingers)

        self.candidates = tuple(new_netlist(idx, value) for idx, value in enumerate(values))

    # pylint: disable=no-self-use
    def get_initial_population(self) -> Sequence[Netlist]:
        return self.candidates

    def get_next_population(
        self, current_candidates: Sequence[Netlist], cost_map: CostMap
    ) -> Sequence[Netlist]:
        return self.candidates


class SingleParamSweep(SearchAlgorithm[Netlist, LibertyResult]):
    """Does 1 simulation that simulates all candidates provided by candidate_generator."""

    def __init__(
        self,
        simulator: Simulator,
        candidate_generator: ParamSweepCandidateGenerator,
        cost_function=noop_cost_function,
    ):
        self._candidate_generator = candidate_generator
        self._cost_function = cost_function
        self._simulate = simulator

    def _should_stop(self) -> bool:
        return self._iteration == 1

    def get_ldb(self) -> LibertyResult:
        return self._simulation_result
