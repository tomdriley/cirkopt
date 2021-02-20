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


class File(IFile):

    def __init__(self, path: str) -> None:
        self.path = path

    def write(self, content: str) -> None:
        with open(self.path, 'w') as writer:
            writer.write(content)

    def read(self) -> str:
        if not os.path.isfile(self.path):
            raise FileNotFoundError(self.path)
        with open(self.path, 'r') as reader:
            file_str = reader.read()
        return file_str
