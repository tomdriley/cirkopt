import os
from dataclasses import dataclass
from abc import ABC, abstractmethod


from src.exceptions import CirkoptFileNotFoundError


@dataclass(eq=True, unsafe_hash=True)  # Force __hash__() generation
class FileData:
    _path: str = ""

    def path(self) -> str:
        return self._path


class FileInterface(ABC):
    @abstractmethod
    def write(self, contents: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self) -> str:
        raise NotImplementedError


# Separate data and interface since MyPy doesn't support abstract dataclasses [1]
# [1] https://github.com/python/mypy/issues/5374
class IFile(FileData, FileInterface):
    @staticmethod
    def from_json(json_dict) -> "IFile":
        if "__File__" in json_dict:
            return File.from_json(json_dict)
        if "__MockFile__" in json_dict:
            return MockFile.from_json(json_dict)
        raise TypeError


@dataclass(eq=False)  # Use parent __eq__(), __hash__()
class File(IFile):
    def write(self, contents: str) -> None:
        with open(self._path, "w") as writer:
            writer.write(contents)

    def read(self) -> str:
        if not os.path.isfile(self._path):
            raise CirkoptFileNotFoundError(self.path)
        with open(self._path, "r") as reader:
            file_str = reader.read()
        return file_str

    def json_repr(self):
        return {"__File__": True, **self.__dict__}

    @staticmethod
    def from_json(json_dict) -> "File":
        if "__File__" in json_dict:
            return File(_path=json_dict["_path"])
        raise TypeError


@dataclass(eq=True, unsafe_hash=True)  # Force __hash__() generation
class MockFile(IFile):
    _contents: str = ""

    def write(self, contents: str) -> None:
        self._contents = contents

    def read(self) -> str:
        return self._contents

    def json_repr(self):
        return {"__MockFile__": True, **self.__dict__}

    @staticmethod
    def from_json(json_dict) -> "MockFile":
        if "__MockFile__" in json_dict:
            return MockFile(_path=json_dict["_path"], _contents=json_dict["_contents"])
        raise TypeError
