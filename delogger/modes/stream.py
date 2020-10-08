from logging import DEBUG, INFO, WARNING
from typing import Dict, List, Optional

from delogger.modes.base import ModeBase

__all__ = [
    "StreamColorDebugMode",
    "StreamDebugMode",
    "StreamInfoMode",
]


class StreamLevelFmt:
    debug: str = "%(levelname)-5s %(asctime)s %(filename)s:%(lineno)d %(message)s"
    info: str = "%(message)s"


class StreamModeBase(ModeBase):
    DATE_FMT: str = "%H:%M:%S"

    def __init__(
        self,
        debug_fmt: Optional[str] = None,
        info_fmt: Optional[str] = None,
        date_fmt: Optional[str] = None,
        stream_level_fmt: StreamLevelFmt = None,
    ) -> None:
        self.debug_fmt = debug_fmt
        self.info_fmt = info_fmt
        self.date_fmt: str = date_fmt or self.DATE_FMT
        self.stream_level_fmt: StreamLevelFmt = stream_level_fmt or StreamLevelFmt()


class StreamDebugMode(StreamModeBase):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def load_to_delogger(self, delogger) -> None:
        debug_fmt = self.stream_level_fmt.debug
        delogger.add_stream_handler(DEBUG, fmt=debug_fmt, datefmt=self.date_fmt)


class StreamInfoMode(StreamModeBase):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def load_to_delogger(self, delogger) -> None:
        debug_fmt = self.stream_level_fmt.debug
        info_fmt = self.stream_level_fmt.info

        delogger.add_stream_handler(INFO, fmt=info_fmt, datefmt=self.date_fmt)


class StreamColorLevelFmt:
    debug: str = StreamLevelFmt.debug.replace(
        "%(levelname)-5s", "%(log_color)s%(levelname)-5s%(reset)s"
    )
    info: str = StreamLevelFmt.info


class StreamColorModeBase(StreamModeBase):
    LOG_COLORS = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARN": "yellow",
        "ERROR": "red",
        "CRIT": "red,bg_white",
    }
    """Definition of color stream level setting."""

    def __init__(
        self,
        stream_color_level_fmt: StreamColorLevelFmt = None,
        log_colors: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.stream_color_level_fmt = stream_color_level_fmt or StreamColorLevelFmt()
        self.log_colors = log_colors or self.LOG_COLORS


class StreamColorDebugMode(StreamColorModeBase):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def load_to_delogger(self, delogger) -> None:
        debug_fmt = self.stream_color_level_fmt.debug

        delogger.add_stream_color_handler(
            DEBUG, log_colors=self.log_colors, fmt=debug_fmt, datefmt=self.date_fmt
        )
