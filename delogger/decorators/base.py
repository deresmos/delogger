from abc import ABC
from abc import abstractmethod
from logging import Logger
from typing import Callable
from typing import Optional


class DecoratorBase(ABC):
    def __init__(self) -> None:
        self.logger: Optional[Logger] = None

    @property
    @abstractmethod
    def decorator_name(self) -> str:
        """decorator name"""

    @abstractmethod
    def wrapper(self, f, *args, **kwargs):
        """wrapper method"""

    def decorator(self, f) -> Callable:
        def wrapper(*args, **kwargs):
            if not self.can_run():
                return f(*args, **kwargs)
            return self.wrapper(f, *args, **kwargs)

        return wrapper

    def load(self, delogger) -> None:
        logger = delogger._logger
        _decorator = getattr(logger, self.decorator_name, None)
        if _decorator:
            raise AttributeError(f"'{self.decorator_name}' already defined.")

        self.logger = logger
        setattr(logger, self.decorator_name, self.decorator)

    def can_run(self) -> bool:
        return True
