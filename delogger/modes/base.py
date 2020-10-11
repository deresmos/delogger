from abc import ABC
from abc import abstractmethod
from typing import Optional

__all__ = ["ModeBase"]


class ModeBase(ABC):
    fmt: str = "%(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self, fmt: Optional[str] = None, datefmt: Optional[str] = None
    ) -> None:
        self.fmt = fmt or self.fmt
        self.datefmt = datefmt or self.datefmt

    @abstractmethod
    def load(self, delogger) -> None:
        pass
