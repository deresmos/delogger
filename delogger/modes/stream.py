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

    STREAM_COLOR_FMTS = [
        STREAM_FMTS[0],
        STREAM_FMTS[1].replace(
            "%(levelname)-5s", "%(log_color)s%(levelname)-5s%(reset)s"
        ),
    ]
    """Default value of color stream logger fmt.(0: normal, 1: debug)"""

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
        is_color: bool = False,
        is_debug: bool = False,
        debug_fmt: Optional[str] = None,
        info_fmt: Optional[str] = None,
        date_fmt: Optional[str] = None,
        stream_fmts: Optional[List[str]] = None,
        stream_color_fmts: Optional[List[str]] = None,
        log_colors: Optional[Dict[str, str]] = None,
    ) -> None:
        self.is_color = is_color
        self.is_debug = is_debug
        self.debug_fmt = debug_fmt
        self.info_fmt = info_fmt
        self.date_fmt = date_fmt or self.DATE_FMT
        self.stream_fmts = stream_fmts or self.STREAM_FMTS
        self.stream_color_fmts = stream_color_fmts or self.STREAM_COLOR_FMTS
        self.log_colors = log_colors or self.LOG_COLORS

    def load_to_delogger(self, delogger):
        debug_fmt = self.debug_fmt or self._stream_fmt(is_debug=True)
        info_fmt = self.info_fmt or self._stream_fmt(is_debug=False)

        if self.is_debug:
            delogger.add_stream_handler(
                DEBUG,
                fmt=debug_fmt,
                is_color_stream=self.is_color,
                datefmt=self.date_fmt,
                log_colors=self.log_colors,
            )
        else:
            delogger.add_stream_handler(
                INFO,
                fmt=info_fmt,
                is_color_stream=self.is_color,
                only_level=True,
                datefmt=self.date_fmt,
                log_colors=self.log_colors,
            )

            delogger.add_stream_handler(
                WARNING,
                fmt=debug_fmt,
                is_color_stream=self.is_color,
                datefmt=self.date_fmt,
                log_colors=self.log_colors,
            )

    def _stream_fmt(self, is_debug: bool):
        """Return a stream fmt."""

        # normal or color fmts.
        fmts = self.stream_color_fmts if self.is_color else self.stream_fmts
        # Info or Debug.
        index = self.FMT_DEBUG_I if is_debug else self.FMT_INFO_I

        return fmts[index]


class ColorStremDebugMode(StreamMode):
    def __init__(self, **kwargs) -> None:
        super().__init__(is_color=True, is_debug=True, **kwargs)


class ColorStreamInfoMode(StreamMode):
    def __init__(self, **kwargs) -> None:
        super().__init__(is_color=True, is_debug=False, **kwargs)


class StreamDebugMode(StreamMode):
    def __init__(self, **kwargs) -> None:
        super().__init__(is_color=False, is_debug=True, **kwargs)


class StreamInfoMode(StreamMode):
    def __init__(self, **kwargs) -> None:
        super().__init__(is_color=False, is_debug=False, **kwargs)
