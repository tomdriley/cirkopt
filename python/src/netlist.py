import re

from dataclasses import dataclass
from typing import Optional, Tuple, Type, TypeVar

from src.file_io import IFile as File
from src.search_algorithm import CandidateClass


SUBCIRKT_NAME_REGEX = r".subckt\s+(.*?)\s+"
WIDTH_REGEX = r"W=(.*?)\s"
LENGTH_REGEX = r"L=(.*?)\s"
FINGERS_REGEX = r"M=(.*?)\s"

ReturnType = TypeVar('ReturnType')


def _extract(text: str, regex: str, return_type: Type[ReturnType]) -> ReturnType:
    match = re.search(regex, text, re.IGNORECASE)
    if match:
        str_value = match.group(1)
        return return_type(str_value)  # type: ignore
    raise ValueError(f"No match of {regex} found in {text}")


def _replace(regex: str, new: str, text: str) -> str:
    return re.sub(regex, new, text, count=1)


class BaseNetlistFile:
    """An immutable view of a netlist file. [Netlist] uses this to avoid duplicating file reads."""

    file: File
    _cached: Optional[str] = None

    def __init__(self, file: File):
        self.file = file

    def contents(self) -> str:
        if self._cached is None:
            self._cached = self.file.read()
        return self._cached


@dataclass(frozen=True)
class Netlist(CandidateClass):
    """Store device characteristics for a given netlist.

    Immutable, so create a new one if you wish change the properties
    """

    base_netlist_file: BaseNetlistFile

    """Cell name"""
    cell_name: str

    """Stores the device widths (in nm) in order of device appearance in base_netlist_file"""
    device_widths: Tuple[float, ...]

    """Stores the device lengths (in nm) in order of device appearance in base_netlist_file"""
    device_lengths: Tuple[float, ...]

    """Stores the device m values in order of device appearance in base_netlist_file"""
    device_fingers: Tuple[int, ...]

    @classmethod
    def create(
        cls,
        base_netlist_file: BaseNetlistFile,
        cell_name: Optional[str] = None,
        device_widths: Optional[Tuple[float, ...]] = None,
        device_lengths: Optional[Tuple[float, ...]] = None,
        device_fingers: Optional[Tuple[int, ...]] = None,
    ):
        netlist_str = base_netlist_file.contents()

        if cell_name is not None:
            cell_name = cell_name
        else:
            cell_name = _extract(netlist_str, SUBCIRKT_NAME_REGEX, str)

        lines = netlist_str.split("\n")
        device_lines = [l + " " for l in lines if len(l) > 0 and l[0].isalpha()]

        if device_widths is not None:
            device_widths = device_widths
        else:
            device_widths = tuple(_extract(l, WIDTH_REGEX, float) for l in device_lines)

        if device_lengths is not None:
            device_lengths = device_lengths
        else:
            device_lengths = tuple(_extract(l, LENGTH_REGEX, float) for l in device_lines)

        if device_fingers is not None:
            device_fingers = device_fingers
        else:
            device_fingers = tuple(_extract(l, FINGERS_REGEX, int) for l in device_lines)
        return cls(base_netlist_file, cell_name, device_widths, device_lengths, device_fingers)

    def key(self) -> str:
        return self.cell_name

    def mutate(
        self,
        cell_name: str,
        device_widths: Tuple[float, ...],
        device_lengths: Tuple[float, ...],
        device_fingers: Tuple[int, ...],
    ) -> "Netlist":
        return Netlist.create(
            base_netlist_file=self.base_netlist_file,
            cell_name=cell_name,
            device_widths=device_widths,
            device_lengths=device_lengths,
            device_fingers=device_fingers,
        )

    def persist(self, file: File) -> None:
        """Writes netlist to new file located via path string."""

        netlist_str = self.base_netlist_file.contents()

        # Update old name to self.cell_name
        old_cell_name = _extract(netlist_str, SUBCIRKT_NAME_REGEX, str)
        new_netlist_str = netlist_str.replace(old_cell_name, self.cell_name)

        lines = new_netlist_str.split("\n")

        current_device = 0
        for i in range(len(lines)):
            device_line = lines[i] + " "
            if len(device_line) == 0 or not device_line[0].isalpha():
                continue

            device_line = _replace(
                regex=WIDTH_REGEX,
                new=f"W={self.device_widths[current_device]} ",
                text=device_line
            )
            device_line = _replace(
                regex=LENGTH_REGEX,
                new=f"L={self.device_lengths[current_device]} ",
                text=device_line
            )
            device_line = _replace(
                regex=FINGERS_REGEX,
                new=f"M={self.device_fingers[current_device]} ",
                text=device_line
            )

            lines[i] = device_line.rstrip()
            current_device += 1

        file.write("\n".join(lines))
