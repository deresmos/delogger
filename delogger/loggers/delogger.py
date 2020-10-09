from logging import Logger
from typing import List, Optional

from delogger.decorators.base import DecoratorBase
from delogger.loggers.base import DeloggerBase
from delogger.modes.base import ModeBase


class Delogger(DeloggerBase):
    def __init__(
        self,
        name: Optional[str] = None,
        modes: Optional[List[ModeBase]] = None,
        decorators: Optional[List[DecoratorBase]] = None,
        **kwargs
    ) -> None:
        super().__init__(name=name, **kwargs)

        if modes:
            self.load_modes(*modes)

        if decorators:
            self.load_decorators(*decorators)

    def get_logger(self) -> Logger:
        if self.is_already_setup():
            return self._logger

        # Set handler
        self._is_new_logger = False

        return self._logger

    def load_modes(self, *modes) -> None:
        if self.is_already_setup():
            return

        for mode in modes:
            mode.load(delogger=self)

    def load_decorators(self, *decorators) -> None:
        if self.is_already_setup():
            return

        for decorator in decorators:
            decorator.load(delogger=self)
