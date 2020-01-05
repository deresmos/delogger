from pathlib import Path

from tests.lib.base import Assert, DeloggerTestBase

from delogger import Delogger
from delogger.modes.stream import (
    StreamColorDebugMode,
    StreamColorInfoMode,
    StreamDebugMode,
    StreamInfoMode,
)


class TestStreamMode(DeloggerTestBase):
    def test_stream_info_mode(self, capsys):
        delogger = Delogger("stream_info_mode")
        delogger.load_modes(StreamInfoMode())
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_normal_stream_log(logger, capsys, is_color=False)

        Assert._bool(not Path(delogger.dirpath).is_dir())

    def test_stream_debug_mode(self, capsys):
        delogger = Delogger(name="stream_debug_mode")
        delogger.load_modes(StreamDebugMode())
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_debug_stream_log(logger, capsys, is_color=False)

        Assert._bool(not Path(delogger.dirpath).is_dir())

    def test_stream_color_info_mode(self, capsys):
        delogger = Delogger(name="stream_color_info_mode")
        delogger.load_modes(StreamColorInfoMode())
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_normal_stream_log(logger, capsys, is_color=True)

        Assert._bool(not Path(delogger.dirpath).is_dir())

    def test_stream_color_debug_mode(self, capsys):
        delogger = Delogger(name="stream_color_debug_mode")
        delogger.load_modes(StreamColorDebugMode())
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_debug_stream_log(logger, capsys, is_color=True)

        Assert._bool(not Path(delogger.dirpath).is_dir())
