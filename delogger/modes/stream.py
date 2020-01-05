from logging import DEBUG, INFO, WARNING
from typing import Dict, List, Optional

from delogger.modes.base import ModeBase

__all__ = [
    "StreamMode",
    "ColorStremDebugMode",
    "ColorStreamInfoMode",
    "StreamDebugMode",
    "StreamInfoMode",
]


class StreamMode(ModeBase):
    DATE_FMT = "%H:%M:%S"

    FMT_INFO_I = 0
    """Info level index constant."""

    FMT_DEBUG_I = 1
    """Debug level index constant."""

    STREAM_FMTS = [
        "%(message)s",
        "%(levelname)-5s %(asctime)s %(filename)s:%(lineno)d %(message)s",
    ]
    """Default value of stream logger fmt.(0: normal, 1: debug)"""

    def __init__(
        self,
        debug_fmt: Optional[str] = None,
        info_fmt: Optional[str] = None,
        date_fmt: Optional[str] = None,
        stream_fmts: Optional[List[str]] = None,
    ) -> None:
        self.debug_fmt = debug_fmt
        self.info_fmt = info_fmt
        self.date_fmt = date_fmt or self.DATE_FMT
        self.stream_fmts = stream_fmts or self.STREAM_FMTS


class ColorStreamMode(StreamMode):
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
        stream_color_fmts: Optional[List[str]] = None,
        log_colors: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.stream_color_fmts = stream_color_fmts or self.make_color_stream_fmts()
        self.log_colors = log_colors or self.LOG_COLORS

    def make_color_stream_fmts(self):
        return [
            self.stream_fmts[self.FMT_INFO_I],
            self.stream_fmts[self.FMT_DEBUG_I].replace(
                "%(levelname)-5s", "%(log_color)s%(levelname)-5s%(reset)s"
            ),
        ]


class ColorStremDebugMode(ColorStreamMode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def load_to_delogger(self, delogger):
        debug_fmt = self.stream_color_fmts[self.FMT_DEBUG_I]

        delogger.add_color_stream_handler(
            DEBUG, log_colors=self.log_colors, fmt=debug_fmt, datefmt=self.date_fmt
        )


class ColorStreamInfoMode(ColorStreamMode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def load_to_delogger(self, delogger):
        debug_fmt = self.stream_color_fmts[self.FMT_DEBUG_I]
        info_fmt = self.stream_color_fmts[self.FMT_INFO_I]

        delogger.add_color_stream_handler(
            INFO,
            log_colors=self.log_colors,
            fmt=info_fmt,
            only_level=True,
            datefmt=self.date_fmt,
        )

        delogger.add_color_stream_handler(
            WARNING, log_colors=self.log_colors, fmt=debug_fmt, datefmt=self.date_fmt
        )


class StreamDebugMode(StreamMode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def load_to_delogger(self, delogger):
        debug_fmt = self.stream_fmts[self.FMT_DEBUG_I]

        delogger.add_stream_handler(DEBUG, fmt=debug_fmt, datefmt=self.date_fmt)


class StreamInfoMode(StreamMode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def load_to_delogger(self, delogger):
        debug_fmt = self.stream_fmts[self.FMT_DEBUG_I]
        info_fmt = self.stream_fmts[self.FMT_INFO_I]

        delogger.add_stream_handler(
            INFO, fmt=info_fmt, only_level=True, datefmt=self.date_fmt
        )

        delogger.add_stream_handler(WARNING, fmt=debug_fmt, datefmt=self.date_fmt)
