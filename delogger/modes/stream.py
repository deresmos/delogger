from logging import DEBUG
from logging import INFO
from typing import Dict
from typing import Optional

from delogger.modes.base import ModeBase

__all__ = [
    "StreamColorDebugMode",
    "StreamDebugMode",
    "StreamInfoMode",
]


class StreamModeBase(ModeBase):
    pass


class StreamDebugMode(StreamModeBase):
    fmt = "%(levelname)-5s | %(message)s"

    def load(self, delogger) -> None:
        delogger.add_stream_handler(DEBUG, fmt=self.fmt, datefmt=self.datefmt)


class StreamInfoMode(StreamModeBase):
    fmt = "%(message)s"

    def load(self, delogger) -> None:
        delogger.add_stream_handler(INFO, fmt=self.fmt, datefmt=self.datefmt)


class StreamColorModeBase(StreamModeBase):
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARN": "yellow",
        "ERROR": "red",
        "CRIT": "red,bg_white",
    }
    """Definition of color stream level setting."""

    def __init__(self, log_colors: Optional[Dict[str, str]] = None, **kwargs) -> None:
        super().__init__(**kwargs)

        self.log_colors = log_colors or self.log_colors


class StreamColorDebugMode(StreamColorModeBase):
    fmt = "%(log_color)s%(levelname)-5s%(reset)s | %(message)s"

    def load(self, delogger) -> None:
        delogger.add_stream_color_handler(
            DEBUG, log_colors=self.log_colors, fmt=self.fmt, datefmt=self.datefmt
        )
