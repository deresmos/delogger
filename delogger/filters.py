class OnlyFilter(object):
    """A filter that performs control to output only the specified level.

    Args:
        level (int): Handler level.

    Attributes:
        _level (int): Handler level.

    """

    def __init__(self, level):
        self._level = level

    def filter(self, record):
        return record.levelno == self._level
