import re

from dataclasses import dataclass
from typing import Optional, Tuple

from src.file_io import IFile as File


SUBCIRKT_NAME_REGEX = r".subckt\s+(.*?)\s+"
DEVICE_WIDTH_REGEX = r"W=(.*?)\s"
DEVICE_LENGTH_REGEX = r"L=(.*?)\s"
DEVICE_FINGERS_REGEX = r"M=(.*?)\s"


def _extract_float(line: str, regex: str) -> float:
    str_value = re.search(regex, line, re.IGNORECASE).group(1)
    return float(str_value)


def _extract_int(line: str, regex: str) -> int:
    str_value = re.search(regex, line, re.IGNORECASE).group(1)
    return int(str_value)


@dataclass()
class BaseNetlistFile:
    """An immutable view of a netlist file. [Netlist] uses this to avoid duplicating file reads."""
    file: File
    _cached: Optional[str] = None

    def contents(self) -> str:
        if self._cached is None:
            self._cached = self.file.read()
        return self._cached


@dataclass(frozen=False)
class Netlist:
    """Store device characteristics for a given netlist.

    Immutable, so create a new one if you wish change the properties
    """
    base_netlist_file: BaseNetlistFile

    """Cell name"""
    cell_name: str

    """Stores the device widths (in nm) in order of device appearance in base_netlist_file"""
    device_widths: Tuple[float]

    """Stores the device lengths (in nm) in order of device appearance in base_netlist_file"""
    device_lengths: Tuple[float]

    """Stores the device m values in order of device appearance in base_netlist_file"""
    device_fingers: Tuple[int]

    def __init__(
            self,
            base_netlist_file: BaseNetlistFile,
            cell_name: Optional[str] = None,
            device_widths: Optional[Tuple[float, ]] = None,
            device_lengths: Optional[Tuple[float, ]] = None,
            device_fingers: Optional[Tuple[int, ]] = None,
    ):
        self.base_netlist_file = base_netlist_file
        netlist_str = self.base_netlist_file.contents()

        if cell_name is not None:
            self.cell_name = cell_name
        else:
            self.cell_name = re.search(SUBCIRKT_NAME_REGEX, netlist_str, re.IGNORECASE).group(1)

        lines = netlist_str.split("\n")
        device_lines = tuple(l + " " for l in lines if len(l) > 0 and l[0].isalpha())

        if device_widths is not None:
            self.device_widths = device_widths
        else:
            self.device_widths = tuple(
                _extract_float(l, DEVICE_WIDTH_REGEX) for l in device_lines
            )

        if device_lengths is not None:
            self.device_lengths = device_lengths
        else:
            self.device_lengths = tuple(
                _extract_float(l, DEVICE_LENGTH_REGEX) for l in device_lines
            )

        if device_fingers is not None:
            self.device_fingers = device_fingers
        else:
            self.device_fingers = tuple(
                _extract_int(l, DEVICE_FINGERS_REGEX) for l in device_lines
            )

    def mutate(
            self,
            cell_name: str,
            device_widths: Tuple[float, ],
            device_lengths: Tuple[float, ],
            device_fingers: Tuple[int, ],
    ) -> 'Netlist':
        return Netlist(
            self.base_netlist_file,
            cell_name,
            device_widths,
            device_lengths,
            device_fingers
        )

    def persist(self, file: File) -> None:
        """Writes netlist to new file located via path string."""

        netlist_str = self.base_netlist_file.contents()

        # Update old name to self.cell_name
        old_netlist_name = re.search(SUBCIRKT_NAME_REGEX, netlist_str, re.IGNORECASE).group(1)
        new_netlist_str = netlist_str.replace(old_netlist_name, self.cell_name)

        lines = new_netlist_str.split("\n")

        current_device = 0
        for i in range(len(lines)):
            device_line = lines[i] + " "
            if len(device_line) == 0 or not device_line[0].isalpha():
                continue

            old_width_str = re.search(DEVICE_WIDTH_REGEX, device_line, re.IGNORECASE).group()
            old_length_str = re.search(DEVICE_LENGTH_REGEX, device_line, re.IGNORECASE).group()
            old_fingers_str = re.search(DEVICE_FINGERS_REGEX, device_line, re.IGNORECASE).group()

            device_line = device_line.replace(
                old_width_str,
                f"W={self.device_widths[current_device]} ",
                1
            )
            device_line = device_line.replace(
                old_length_str,
                f"L={self.device_lengths[current_device]} ",
                1
            )
            device_line = device_line.replace(
                old_fingers_str,
                f"M={self.device_fingers[current_device]} ",
                1
            )

            lines[i] = device_line.rstrip()
            current_device += 1

        file.write("\n".join(lines))
