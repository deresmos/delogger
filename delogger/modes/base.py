from abc import ABCMeta, abstractmethod

__all__ = ["ModeBase"]


class ModeBase(metaclass=ABCMeta):
    @abstractmethod
    def load_to_delogger(self, base) -> None:
        pass
