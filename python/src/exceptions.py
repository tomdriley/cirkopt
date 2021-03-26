class CirkoptException(Exception):
    pass


class CirkoptValueError(ValueError, CirkoptException):
    pass
