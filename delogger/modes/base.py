from abc import ABCMeta, abstractmethod


class ModeBase(metaclass=ABCMeta):
    @abstractmethod
    def load_to_delogger(self, base) -> None:
        pass
