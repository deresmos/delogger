from tests.lib.base import DeloggerTestBase
from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.modes.stream import StreamColorDebugMode


class TestDelogger(DeloggerTestBase):
    def test_delogger(self, capsys):
        delogger = Delogger("test_delogger")
        delogger.load_modes(StreamColorDebugMode())
        delogger.load_decorators(DebugLog())

        logger = delogger.get_logger()

        self.execute_log(logger)

        self.check_debug_stream_log(logger, capsys, is_color=True)

        assert getattr(logger, "debuglog")

    def test_delogger_constructor(self, capsys):
        delogger = Delogger(
            name="test_delogger_c",
            modes=[StreamColorDebugMode()],
            decorators=[DebugLog()],
        )

        logger = delogger.get_logger()

        self.execute_log(logger)

        self.check_debug_stream_log(logger, capsys, is_color=True)

        assert getattr(logger, "debuglog")
