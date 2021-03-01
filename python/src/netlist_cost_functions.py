from typing import Sequence, Any

from src.search_algorithm import CostFunction, CostMap
from src.netlist import Netlist


def noop_cost_function(
    candidates: Sequence[Netlist], simulation_result: Any
) -> CostMap:
    """Noop cost function"""
    return {candidate.key(): 0.0 for candidate in candidates}