from abc import ABCMeta, abstractmethod

from delogger.base import DeloggerBase


class ModeBase(metaclass=ABCMeta):
    @abstractmethod
    def load_to_delogger(self, base: DeloggerBase) -> None:
        pass
