class OnlyFilter(object):
    def __init__(self, level):
        self._level = level

    def filter(self, record):
        return record.levelno == self._level
