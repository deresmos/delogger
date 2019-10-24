from abc import ABCMeta, abstractmethod

from delogger.base import DeloggerBase


class ModeBase(metaclass=ABCMeta):
    @abstractmethod
    def load_mode(self, base: DeloggerBase) -> None:
        pass


class PropagateMode(metaclass=ABCMeta):
    def load_mode(self, delogger: DeloggerBase) -> None:
        delogger._logger.propagate = True
