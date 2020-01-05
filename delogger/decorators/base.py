from abc import ABCMeta, abstractmethod
from logging import Logger
from typing import Optional

from delogger.base import DeloggerBase


class DecoratorBase(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.logger: Optional[Logger] = None

    @property
    @abstractmethod
    def decorator_name(self) -> str:
        pass

    @abstractmethod
    def decorator(self, func):
        pass

    def load_to_delogger(self, delogger: DeloggerBase) -> None:
        logger = delogger._logger
        _decorator = getattr(logger, self.decorator_name, None)
        if _decorator:
            raise AttributeError(f"'{self.decorator_name}' already defined.")

        self.logger = logger
        setattr(logger, self.decorator_name, self.decorator)
