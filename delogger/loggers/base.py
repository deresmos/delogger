from logging import CRITICAL
from logging import DEBUG
from logging import Formatter
from logging import Logger
from logging import StreamHandler
from logging import WARNING
from logging import addLevelName
from logging import getLogger
import os
from typing import Dict
from typing import List
from typing import Optional

from colorlog import ColoredFormatter

from delogger.decorators.base import DecoratorBase
from delogger.filters.only_filter import OnlyFilter
from delogger.modes.base import ModeBase


class DeloggerBase:
    """A class that provides a decided logger.

    Args:
        name (str): Logger name
        parent (str): Log file save destination.
        *args: DeloggerSetting.
        **kwargs: DeloggerSetting.

    Attributes:
        _logger (logging.Logger): Logger.
        _is_new_logger (bool): Whether it is a first generation logger.

    """

    def __init__(
        self,
        name: Optional[str] = None,
        modes: Optional[List[ModeBase]] = None,
        decorators: Optional[List[DecoratorBase]] = None,
    ) -> None:
        addLevelName(WARNING, "WARN")
        addLevelName(CRITICAL, "CRIT")

        # base logger
        name = name or os.getenv("DELOGGER_NAME", "delogger")
        logger = getLogger(name)
        logger.setLevel(DEBUG)
        self._logger: Logger = logger

        # check already set logger
        if len(self._logger.handlers) > 0:
            # Already set logger
            self._is_new_logger = False
        else:
            # Not set logger
            self._is_new_logger = True

        if not self.is_already_setup():
            if modes:
                self.load_modes(*modes)

            if decorators:
                self.load_decorators(*decorators)

    def get_logger(self) -> Logger:
        if self.is_already_setup():
            return self._logger

        self._is_new_logger = False

        return self._logger

    def load_mode(self, mode: ModeBase) -> None:
        mode.load(delogger=self)

    def load_modes(self, *modes) -> None:
        for mode in modes:
            self.load_mode(mode)

    def load_decorator(self, decorator: DecoratorBase) -> None:
        decorator.load(delogger=self)

    def load_decorators(self, *decorators) -> None:
        for decorator in decorators:
            self.load_decorator(decorator)

    def is_already_setup(self) -> bool:
        return not self._is_new_logger

    def add_handler(
        self,
        hdlr,
        level: int,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        only_level: bool = False,
        formatter=None,
    ) -> None:
        """Helper function to add a handler.

        Args:
            hdlr: handler
            level (int): Handler level.
            fmt (str): Handler output format.
            datefmt (str): Handler output date format.
            only_level (bool): Whether to output only to specified han-
            dler level.
            formatter: Handler formatter.

        """

        hdlr.setLevel(level)

        # Set formatter.
        formatter = formatter or Formatter(fmt, datefmt)
        hdlr.setFormatter(formatter)

        if only_level:
            hdlr.addFilter(OnlyFilter(level))

        self._logger.addHandler(hdlr)

    def add_stream_handler(self, level: int, *, hdlr=None, **kwargs) -> None:
        """Helper function to add a stream handler.

        Args:
            level (int): Handler level.
            hdlr: Handler other than stream handler.
            **kwargs: Keyword argument of add_handler method

        """

        hdlr = hdlr or StreamHandler()
        self.add_handler(hdlr, level, **kwargs)

    def add_stream_color_handler(
        self,
        level: int,
        log_colors: Optional[Dict[str, str]],
        *,
        hdlr=None,
        datefmt: Optional[str] = None,
        **kwargs
    ) -> None:
        """Helper function to add a color stream handler.

        Args:
            level (int): Handler level.
            hdlr: Handler other than stream handler.
            **kwargs: Keyword argument of add_handler method

        """

        formatter = ColoredFormatter(
            kwargs.get("fmt", None), log_colors=log_colors, style="%", datefmt=datefmt
        )

        hdlr = hdlr or StreamHandler()
        self.add_handler(hdlr, level, datefmt=datefmt, formatter=formatter, **kwargs)

    @property
    def propagate(self) -> bool:
        return self._logger.propagate

    @propagate.setter
    def propagate(self, is_propagate: bool) -> None:
        self._logger.propagate = is_propagate
