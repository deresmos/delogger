from delogger import Delogger
from delogger.decorators.profiles import LineMemoryProfile, LineProfile, MemoryProfile
from delogger.modes.stream import StreamDebugMode
from tests.lib.base import DeloggerTestBase


class TestProfileDecorator(DeloggerTestBase):
    def test_line_profile_decorator(self, capsys, caplog):
        delogger = Delogger("line_profile_decorator", modes=[StreamDebugMode()])
        delogger.load_decorators([LineProfile()])
        logger = delogger.get_logger()

        @logger.line_profile
        def test_func(arg1, arg2=None):
            pass

        # Only execute
        test_func("testarg", 123)

    def test_memory_profile_decorator(self, capsys, caplog):
        delogger = Delogger("memory_profile_decorator", modes=[StreamDebugMode()])
        delogger.load_decorators([MemoryProfile()])
        logger = delogger.get_logger()

        @logger.memory_profile
        def test_func(arg1, arg2=None):
            pass

        # Only execute
        test_func("testarg", 123)

    def test_line_memory_profile_decorator(self, capsys, caplog):
        delogger = Delogger("line_memory_profile_decorator", modes=[StreamDebugMode()])
        delogger.load_decorators([LineMemoryProfile()])
        logger = delogger.get_logger()

        @logger.line_memory_profile
        def test_func(arg1, arg2=None):
            pass

        # Only execute
        test_func("testarg", 123)
