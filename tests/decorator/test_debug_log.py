from delogger import Delogger
from delogger.decorator.debug_log import DebugLog
from delogger.mode.stream import StreamDebugMode
from tests.lib.base import Assert
from tests.lib.base import DeloggerTestBase


class TestDebugLogDecorator(DeloggerTestBase):
    def test_debug_log_decorator(self, capsys, caplog):
        delogger = Delogger("debug_log_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(DebugLog())
        logger = delogger.get_logger()

        @logger.debuglog
        def test_func(arg1, arg2=None):
            pass

        test_func("testarg", 123)

        streams = [
            r"START TestDebugLogDecorator.test_debug_log_decorator.<locals>.test_func args=\('testarg', 123\) kwargs={}",
            r"END TestDebugLogDecorator.test_debug_log_decorator.<locals>.test_func return=None",
        ]
        self.check_decorator(logger, capsys, streams)

    def check_decorator(self, logger, capsys, streams):
        captured = capsys.readouterr()
        fmt = self.DEBUG_FMT
        streams = [fmt % stream for stream in streams]
        logs = captured.err.split("\n")
        for stream, log in zip(streams, logs):
            Assert._match(stream, log)
        return False
