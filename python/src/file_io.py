import os
from abc import ABCMeta, abstractmethod


class IFile:
    __metaclass__ = ABCMeta
    path: str

    @abstractmethod
    def write(self, content: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self) -> str:
        raise NotImplementedError

    @staticmethod
    def from_json(json_dict):
        if "__File__" in json_dict:
            return File.from_json(json_dict)
        raise TypeError


class File(IFile):
    def __init__(self, path: str) -> None:
        self.path = path

    def write(self, content: str) -> None:
        with open(self.path, "w") as writer:
            writer.write(content)

    def read(self) -> str:
        if not os.path.isfile(self.path):
            raise FileNotFoundError(self.path)
        with open(self.path, "r") as reader:
            file_str = reader.read()
        return file_str

    def json_repr(self):
        return {"__File__": True, "path": self.path}

    @staticmethod
    def from_json(json_dict) -> "File":
        if "__File__" in json_dict:
            return File(json_dict["path"])
        raise TypeError
