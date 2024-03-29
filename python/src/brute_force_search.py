from dataclasses import dataclass
from math import ceil, log10
from typing import Iterator, List, Sequence
from decimal import Decimal

from src.circuit_search_common import Range
from src.liberty_parser import LibertyResult
from src.netlist import Netlist
from src.search_algorithm import (
    CandidateGenerator,
    CostMap,
    SearchAlgorithm,
    Simulator,
    CostFunction,
)
from src.utils import chunked


@dataclass(frozen=True)
class BruteForceCandidateGenerator(CandidateGenerator[Netlist]):
    # pylint: disable=too-many-instance-attributes
    widths: Sequence[float]
    lengths: Sequence[float]
    fingers: Sequence[int]

    reference_netlist: Netlist

    ndigits: int
    ndevices: int
    generator: Iterator[Sequence[Sequence[int]]]

    @classmethod
    def create(
        cls,
        reference_netlist: Netlist,
        width_range: Range[Decimal],
        length_range: Range[Decimal],
        fingers_range: Range[int],
        simulations_per_iteration: int,
    ) -> "BruteForceCandidateGenerator":
        widths = tuple(map(float, width_range))
        lengths = tuple(map(float, length_range))
        fingers = tuple(fingers_range)
        ndevices = len(reference_netlist.device_widths)
        generator = cls._get_generator(widths, lengths, fingers, ndevices)
        return cls(
            widths=widths,
            lengths=lengths,
            fingers=fingers,
            reference_netlist=reference_netlist,
            ndigits=ceil(log10(simulations_per_iteration)),
            ndevices=ndevices,
            generator=chunked(generator, simulations_per_iteration),
        )

    @staticmethod
    def _get_generator(
        widths: Sequence[float], lengths: Sequence[float], fingers: Sequence[int], ndevices: int
    ) -> Iterator[Sequence[int]]:
        normalized_netlist = [0] * (3 * ndevices)
        terminal_vals = [
            len(widths) - 1
            if 0 <= idx < ndevices
            else len(lengths) - 1
            if ndevices <= idx < 2 * ndevices
            else len(fingers) - 1
            for idx in range(len(normalized_netlist))
        ]

        def increment_netlist(netlist: List[int]) -> List[int]:
            copy = netlist.copy()
            carry = 1
            for idx in range(len(copy)):
                if carry == 0:
                    break

                if copy[idx] == terminal_vals[idx]:
                    new_val = 0
                    carry = 1
                else:
                    new_val = copy[idx] + 1
                    carry = 0
                copy[idx] = new_val
            return copy

        yield normalized_netlist
        while not all(
            normalized_netlist[idx] == terminal_vals[idx] for idx in range(len(normalized_netlist))
        ):
            normalized_netlist = increment_netlist(normalized_netlist)
            yield normalized_netlist

    def _denomalize(self, normalized_netlist: Sequence[int], _id: int) -> Netlist:
        base_name = self.reference_netlist.cell_name
        name = base_name + "_" + str(_id).zfill(self.ndigits)
        ndevices = self.ndevices
        return self.reference_netlist.clone(
            cell_name=name,
            device_widths=tuple(
                self.widths[width_idx] for width_idx in normalized_netlist[:ndevices]
            ),
            device_lengths=tuple(
                self.lengths[length_idx] for length_idx in normalized_netlist[ndevices:-ndevices]
            ),
            device_fingers=tuple(
                self.fingers[fingers_idx] for fingers_idx in normalized_netlist[-ndevices:]
            ),
        )

    # pylint: disable=no-self-use
    def get_initial_population(self) -> Sequence[Netlist]:
        return self.get_next_population(tuple(), dict())

    def get_next_population(
        self, current_candidates: Sequence[Netlist], cost_map: CostMap
    ) -> Sequence[Netlist]:
        try:
            return tuple(
                self._denomalize(netlist, _id) for _id, netlist in enumerate(next(self.generator))
            )
        except StopIteration:
            return tuple()


class BruteForceSearch(SearchAlgorithm[Netlist, LibertyResult]):
    """Simulates until BruteForceCandidateGenerator runs out of candidates."""

    def __init__(
        self,
        candidate_generator: BruteForceCandidateGenerator,
        cost_function: CostFunction,
        simulator: Simulator,
    ):
        self._candidate_generator = candidate_generator
        self._cost_function = cost_function
        self._simulate = simulator

    def _should_stop(self) -> bool:
        return False  # go until run out of candidates
