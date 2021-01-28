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
        raise NotImplementedError("TODO: write content to file path")

    def read(self) -> str:
        raise NotImplementedError("TODO: read content from file path")
