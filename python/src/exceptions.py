class CirkoptException(Exception):
    pass


class CirkoptValueError(ValueError, CirkoptException):
    pass


class CirkoptFileNotFoundError(FileNotFoundError, CirkoptException):
    pass


class CirkoptNotADirectoryError(NotADirectoryError, CirkoptException):
    pass
