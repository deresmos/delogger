from pathlib import Path

from delogger import Delogger
from delogger.modes.stream import (
    ColorStreamInfoMode,
    ColorStremDebugMode,
    StreamDebugMode,
    StreamInfoMode,
)
from tests.lib.base import Assert, DeloggerTestBase


class TestStreamMode(DeloggerTestBase):
    def test_stream_info_mode(self, capsys):
        delogger = Delogger("stream_info_mode", modes=[StreamInfoMode()])
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_normal_stream_log(logger, capsys, is_color=False)

        Assert._bool(not Path(delogger.dirpath).is_dir())

    def test_stream_debug_mode(self, capsys):
        delogger = Delogger(name="stream_debug_mode", modes=[StreamDebugMode()])
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_debug_stream_log(logger, capsys, is_color=False)

        Assert._bool(not Path(delogger.dirpath).is_dir())

    def test_color_stream_info_mode(self, capsys):
        delogger = Delogger(
            name="color_stream_info_mode", modes=[ColorStreamInfoMode()]
        )
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_normal_stream_log(logger, capsys, is_color=True)

        Assert._bool(not Path(delogger.dirpath).is_dir())

    def test_color_stream_debug_mode(self, capsys):
        delogger = Delogger(
            name="color_stream_debug_mode", modes=[ColorStremDebugMode()]
        )
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_debug_stream_log(logger, capsys, is_color=True)

        Assert._bool(not Path(delogger.dirpath).is_dir())
