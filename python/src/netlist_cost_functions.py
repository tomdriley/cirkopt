from typing import Sequence, Any, Tuple
from itertools import chain

from src.search_algorithm import CostMap
from src.netlist import Netlist
from src.liberty_parser import LibertyResult, Group


def noop_cost_function(
    candidates: Sequence[Netlist],
    simulation_result: Any,  # pylint: disable=unused-argument
) -> CostMap:
    """Noop cost function"""
    return {candidate.key(): 0.0 for candidate in candidates}


def longest_delay(cell: Group, delay_idx: Tuple[int, int]) -> float:
    assert hasattr(cell, "pin")
    # Get list of output pins, e.g. usually just <Y>
    output_pins = (pin for pin in cell.pin if pin.direction == "output")
    # Get all possible timing arcs, e.g. <A -> Y>, <B -> Y> for NAND or NOR
    # python magic to unroll 2D array
    timing_arcs = (timing for pin in output_pins for timing in pin.timing)
    # Corresponding rising delay for each arch
    rise_delays = (
        timing_arc.cell_rise[0].values[delay_idx[0]][delay_idx[1]]
        for timing_arc in timing_arcs
    )
    # Corresponding falling delay for each arch
    fall_delays = (
        timing_arc.cell_fall[0].values[delay_idx[0]][delay_idx[1]]
        for timing_arc in timing_arcs
    )
    # Concenate lists to get list of all possible delays
    delays = chain(rise_delays, fall_delays)
    # Return worst case timing arch
    return max(delays)


def delay_cost_function(
    candidates: Sequence[Netlist],
    simulation_result: LibertyResult,
    delay_idx: Tuple[int, int],
) -> CostMap:
    """ Longest delay """
    cost_map = {
        cell.name: longest_delay(cell, delay_idx) for cell in simulation_result.cell
    }

    for candidate in candidates:
        if candidate.key() not in cost_map:
            raise ValueError("Not all candidates have a simulation result")

    return cost_map
