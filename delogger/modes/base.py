from abc import ABCMeta, abstractmethod

from delogger.base import DeloggerBase


class ModeBase(metaclass=ABCMeta):
    @abstractmethod
    def load_handler(self, base: DeloggerBase) -> None:
        pass


class PropagateMode(metaclass=ABCMeta):
    def load_handler(self, delogger: DeloggerBase) -> None:
        delogger._logger.propagate = True
