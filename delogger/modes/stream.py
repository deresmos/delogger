from logging import DEBUG, INFO, WARNING
from typing import Optional

from delogger.base import DeloggerBase
from delogger.modes.base import ModeBase

__all__ = [
    "StreamMode",
    "ColorStremDebugMode",
    "ColorStreamInfoMode",
    "StreamDebugMode",
    "StreamInfoMode",
]


class StreamMode(ModeBase):
    def __init__(
        self,
        is_color: bool = False,
        is_debug: bool = False,
        debug_fmt: Optional[str] = None,
        info_fmt: Optional[str] = None,
    ) -> None:
        self.is_color = is_color
        self.is_debug = is_debug
        self.debug_fmt = debug_fmt
        self.info_fmt = info_fmt

    def load_handler(self, delogger: DeloggerBase):
        debug_fmt = self.debug_fmt or self._stream_fmt(delogger, is_debug=True)
        info_fmt = self.info_fmt or self._stream_fmt(delogger, is_debug=False)

        if self.is_debug:
            delogger.add_stream_handler(
                DEBUG, fmt=debug_fmt, is_color_stream=self.is_color
            )
        else:
            delogger.add_stream_handler(
                INFO, fmt=info_fmt, is_color_stream=self.is_color, only_level=True
            )

            delogger.add_stream_handler(
                WARNING, fmt=debug_fmt, is_color_stream=self.is_color
            )

    def _stream_fmt(self, delogger, is_debug: bool):
        """Return a stream fmt."""

        # normal or color fmts.
        fmts = delogger.stream_color_fmts if self.is_color else delogger.stream_fmts
        # Info or Debug.
        index = delogger.FMT_DEBUG if is_debug else delogger.FMT_INFO

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
