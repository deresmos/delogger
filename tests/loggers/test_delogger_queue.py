from delogger import DeloggerQueue
from delogger.decorators.debug_log import DebugLog
from delogger.modes.stream import StreamDebugMode
from tests.lib.base import DeloggerTestBase


class TestDeloggerQueue(DeloggerTestBase):
    def test_delogger_queue_base(self, capsys):
        delogger = DeloggerQueue(
            name="delogger_queue_base",
        )

        assert delogger.join() is False
        assert delogger._find_queue_hdlr(delogger._logger.handlers) is None

        logger = delogger.get_logger()

        logger.debug("debug")
        assert delogger.join() is True

    def test_delogger_queue(self, capsys):
        delogger = DeloggerQueue("test_delogger_queue")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(DebugLog())

        logger = delogger.get_logger()

        self.execute_log(logger)

        delogger.join()
        self.check_debug_stream_log(logger, capsys, is_color=False)

        assert getattr(logger, "debuglog")

        delogger = DeloggerQueue("test_delogger_queue")

        logger = delogger.get_logger()

        self.execute_log(logger)

        delogger.join()
        self.check_debug_stream_log(logger, capsys, is_color=False)

        assert getattr(logger, "debuglog")

    def test_delogger_queue_constructor(self, capsys):
        delogger = DeloggerQueue(
            name="test_delogger_queue_c",
            modes=[StreamDebugMode()],
            decorators=[DebugLog()],
        )

        logger = delogger.get_logger()

        self.execute_log(logger)

        delogger.join()
        self.check_debug_stream_log(logger, capsys, is_color=False)

        assert getattr(logger, "debuglog")
