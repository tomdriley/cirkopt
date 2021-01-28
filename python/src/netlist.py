from dataclasses import dataclass
from typing import Optional, Tuple
from file_io import IFile as File


@dataclass()
class BaseNetlistFile:
    """An immutable view of a netlist file. [Netlist] uses this to avoid duplicating file reads."""
    file: File
    _cached: Optional[str] = None

    def contents(self) -> str:
        if self._cached is None:
            self._cached = self.file.read()
        return self._cached


@dataclass(frozen=True)
class Netlist:
    """Store device characteristics for a given netlist.

    Immutable, so create a new one if you wish change the properties
    """
    base_netlist_file: BaseNetlistFile

    """Stores the device widths (in nm) in order of device appearance in base_netlist_file"""
    device_widths: Tuple[int]

    """Stores the device lengths (in nm) in order of device appearance in base_netlist_file"""
    device_lengths: Tuple[int]

    """Stores the device m values in order of device appearance in base_netlist_file"""
    device_m_values: Tuple[int]

    def persist(self, file: File) -> None:
        """Writes netlist to new file located via path string."""
        raise NotImplementedError("TODO: read base_netlist_file, modify, and write to file")
