from delogger import Delogger
from delogger.decorator.profiles import (
    LineMemoryProfile,
    LineProfile,
    LineProfileStats,
    MemoryProfile,
)
from delogger.mode.stream import StreamDebugMode
from tests.lib.base import DeloggerTestBase


class TestProfileDecorator(DeloggerTestBase):
    def test_line_profile_decorator(self, capsys, caplog):
        try:
            import line_profiler  # noqa
        except ImportError:
            return

        delogger = Delogger("line_profile_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(LineProfile())
        logger = delogger.get_logger()

        @logger.line_profile
        def test_func(arg1, arg2=None):
            pass

        # Only execute
        test_func("testarg", 123)

    def test_line_profile_stats_decorator(self, capsys, caplog):
        try:
            import line_profiler  # noqa
        except ImportError:
            return

        delogger = Delogger("line_profile_stats_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(LineProfileStats())
        logger = delogger.get_logger()

        @logger.add_line_profile
        def test_func(arg1, arg2=None):
            pass

        # Only execute
        test_func("testarg", 123)

    def test_memory_profile_decorator(self, capsys, caplog):
        try:
            import memory_profiler  # noqa
        except ImportError:
            return

        delogger = Delogger("memory_profile_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(MemoryProfile())
        logger = delogger.get_logger()

        @logger.memory_profile
        def test_func(arg1, arg2=None):
            pass

        # Only execute
        test_func("testarg", 123)

    def test_line_memory_profile_decorator(self, capsys, caplog):
        try:
            import line_profiler  # noqa
        except ImportError:
            return

        delogger = Delogger("line_memory_profile_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(LineMemoryProfile())
        logger = delogger.get_logger()

        @logger.line_memory_profile
        def test_func(arg1, arg2=None):
            pass

        # Only execute
        test_func("testarg", 123)
