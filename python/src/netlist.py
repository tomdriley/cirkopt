import re

from dataclasses import dataclass, field
from typing import Optional, Tuple, Type, TypeVar, Any

from src.file_io import IFile as File
from src.search_algorithm import CandidateClass
from src.exceptions import CirkoptValueError, CirkoptException


SUBCIRKT_NAME_REGEX = r".subckt\s+(.*?)\s+"
# 1 or more digits, optionally followed by a '.' with one or more digits optionally followed by '+' or '-'
# followed by e and one or more digits
SCI_NOTATION = r"(\d+(?:\.\d+)?e[-\+]?\d+)"
WIDTH_REGEX = r"W=" + SCI_NOTATION
LENGTH_REGEX = r"L=" + SCI_NOTATION
FINGERS_REGEX = r"M=(\d+)"

ReturnType = TypeVar("ReturnType")


def _extract(text: str, regex: str, return_type: Type[ReturnType]) -> ReturnType:
    match = re.search(regex, text, re.IGNORECASE)
    if match:
        str_value = match.group(1)
        return return_type(str_value)  # type: ignore
    raise CirkoptValueError(f"No match of {regex} found in {text}")


def _replace(regex: str, new: str, text: str) -> str:
    return re.sub(regex, new, text, count=1)


@dataclass(frozen=True)
class BaseNetlistFile:
    """An immutable view of a netlist file. [Netlist] uses this to avoid duplicating file reads."""

    _path: str
    _contents: str

    @classmethod
    def create(cls: Type["BaseNetlistFile"], file: File) -> "BaseNetlistFile":
        path = file.path()
        contents = file.read()
        return cls(_contents=contents, _path=path)

    def contents(self) -> str:
        return self._contents

    def json_repr(self):
        return {"__BaseNetlistFile__": True, **self.__dict__}

    @staticmethod
    def from_json(json_dict) -> "BaseNetlistFile":
        if "__BaseNetlistFile__" in json_dict:
            return BaseNetlistFile(_contents=json_dict["_contents"], _path=json_dict["_path"])
        raise TypeError


@dataclass(frozen=True)
class Netlist(CandidateClass):
    """Store device characteristics for a given netlist.

    Immutable, so create a new one if you wish change the properties
    """

    base_netlist_file: BaseNetlistFile

    """Cell name"""
    cell_name: str = field(compare=False, hash=None)

    """Stores the device widths (in nm) in order of device appearance in base_netlist_file"""
    device_widths: Tuple[float, ...]

    """Stores the device lengths (in nm) in order of device appearance in base_netlist_file"""
    device_lengths: Tuple[float, ...]

    """Stores the device m values in order of device appearance in base_netlist_file"""
    device_fingers: Tuple[int, ...]

    @classmethod
    def create(
        cls: Type["Netlist"],
        base_netlist_file: BaseNetlistFile,
        cell_name: Optional[str] = None,
        device_widths: Optional[Tuple[float, ...]] = None,
        device_lengths: Optional[Tuple[float, ...]] = None,
        device_fingers: Optional[Tuple[int, ...]] = None,
    ) -> "Netlist":
        netlist_str = base_netlist_file.contents()
        if len(netlist_str.strip(" \n")) < 1:
            raise CirkoptException("Empty netlist file")

        if cell_name is None:
            cell_name = _extract(netlist_str, SUBCIRKT_NAME_REGEX, str)

        lines = netlist_str.split("\n")
        device_lines = [l + " " for l in lines if len(l) > 0 and l[0].isalpha()]
        if len(device_lines) < 1:
            raise CirkoptException("Invalid netlist, no device lines found")

        if device_widths is None:
            device_widths = tuple(_extract(l, WIDTH_REGEX, float) for l in device_lines)

        if device_lengths is None:
            device_lengths = tuple(_extract(l, LENGTH_REGEX, float) for l in device_lines)

        if device_fingers is None:
            device_fingers = tuple(_extract(l, FINGERS_REGEX, int) for l in device_lines)
        return cls(base_netlist_file, cell_name, device_widths, device_lengths, device_fingers)

    def key(self) -> str:
        return self.cell_name

    def clone(
        self,
        cell_name: Optional[str] = None,
        device_widths: Optional[Tuple[float, ...]] = None,
        device_lengths: Optional[Tuple[float, ...]] = None,
        device_fingers: Optional[Tuple[int, ...]] = None,
    ) -> "Netlist":
        if cell_name is None:
            cell_name = self.cell_name
        if device_widths is None:
            device_widths = self.device_widths
        if device_lengths is None:
            device_lengths = self.device_lengths
        if device_fingers is None:
            device_fingers = self.device_fingers

        # Ensure we're creating valid netlists
        assert len(cell_name) > 0
        assert len(device_widths) > 0 and len(device_lengths) > 0 and len(device_fingers) > 0

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
            device_line = lines[i]
            if len(device_line) == 0 or not device_line[0].isalpha():
                continue

            device_line = _replace(
                regex=WIDTH_REGEX, new=f"W={self.device_widths[current_device]}", text=device_line
            )
            device_line = _replace(
                regex=LENGTH_REGEX,
                new=f"L={self.device_lengths[current_device]}",
                text=device_line,
            )
            device_line = _replace(
                regex=FINGERS_REGEX,
                new=f"M={self.device_fingers[current_device]}",
                text=device_line,
            )

            lines[i] = device_line.rstrip()
            current_device += 1

        file.write("\n".join(lines))

    def json_repr(self):
        return {"__Netlist__": True, **self.__dict__}

    @staticmethod
    def from_json(json_dict) -> Any:
        if "__Netlist__" in json_dict:
            return Netlist.create(
                base_netlist_file=json_dict["base_netlist_file"],
                cell_name=json_dict["cell_name"],
                device_widths=tuple(json_dict["device_widths"]),
                device_lengths=tuple(json_dict["device_lengths"]),
                device_fingers=tuple(json_dict["device_fingers"]),
            )
        return BaseNetlistFile.from_json(json_dict)
