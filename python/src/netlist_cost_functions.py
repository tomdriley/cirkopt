from typing import Sequence, Any

from src.search_algorithm import CostFunction, CostMap
from src.netlist import Netlist


class NoopCostFunction(CostFunction[Netlist, Any]):
    """Noop cost function"""

    # pylint: disable=no-self-use,unused-argument
    def calculate(
        self, candidates: Sequence[Netlist], simulation_result: Any
    ) -> CostMap:
        return {candidate.key(): 0.0 for candidate in candidates}