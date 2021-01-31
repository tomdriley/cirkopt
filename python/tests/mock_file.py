from file_io import IFile


class MockFile(IFile):
    content: str = ""

    def write(self, content: str) -> None:
        self.content = content

    def read(self) -> str:
        return self.content
