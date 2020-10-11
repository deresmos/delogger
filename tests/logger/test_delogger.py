from delogger import Delogger
from delogger.decorator.debug_log import DebugLog
from delogger.mode.stream import StreamDebugMode
from tests.lib.base import DeloggerTestBase


class TestDelogger(DeloggerTestBase):
    def test_delogger(self, capsys):
        delogger = Delogger("test_delogger")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(DebugLog())

        logger = delogger.get_logger()

        self.execute_log(logger)

        self.check_debug_stream_log(logger, capsys, is_color=False)

        assert getattr(logger, "debuglog")

        delogger = Delogger("test_delogger")
        logger = delogger.get_logger()

        self.execute_log(logger)

        self.check_debug_stream_log(logger, capsys, is_color=False)

        assert getattr(logger, "debuglog")

    def test_delogger_constructor(self, capsys):
        delogger = Delogger(
            name="test_delogger_c",
            modes=[StreamDebugMode()],
            decorators=[DebugLog()],
        )

        logger = delogger.get_logger()

        self.execute_log(logger)

        self.check_debug_stream_log(logger, capsys, is_color=False)

        assert getattr(logger, "debuglog")
