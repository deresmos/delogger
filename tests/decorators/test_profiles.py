from delogger import Delogger
import delogger.decorators.line_memory_profile
import delogger.decorators.line_profile
from delogger.decorators.profiles import LineMemoryProfile
from delogger.decorators.profiles import LineProfile
from delogger.decorators.profiles import LineProfileStats
from delogger.decorators.profiles import MemoryProfile
from delogger.modes.stream import StreamDebugMode
from tests.lib.base import DeloggerTestBase


class TestProfileDecorator(DeloggerTestBase):
    def setup_class(self):
        # avoid line_profiler/issues/16
        delogger.decorators.line_profile._can_line_profiler = False
        delogger.decorators.line_memory_profile._can_line_profiler = False

    def test_line_profile_decorator(self):
        delogger = Delogger("line_profile_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(LineProfile())
        logger = delogger.get_logger()

        @logger.line_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

    def test_line_profile_stats_decorator(self, capsys, caplog):
        delogger = Delogger("line_profile_stats_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(LineProfileStats())
        logger = delogger.get_logger()

        @logger.add_line_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

    def test_memory_profile_decorator(self, capsys, caplog):
        delogger = Delogger("memory_profile_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(MemoryProfile())
        logger = delogger.get_logger()

        @logger.memory_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

    def test_memory_profile_decorator_no_module(self, capsys, caplog):
        import delogger.decorators.memory_profile

        _tmp = delogger.decorators.memory_profile._can_memory_profiler
        delogger.decorators.memory_profile._can_memory_profiler = False

        _delogger = Delogger("memory_profile_decorator_no_module")
        _delogger.load_modes(StreamDebugMode())
        _delogger.load_decorators(MemoryProfile())
        logger = _delogger.get_logger()

        @logger.memory_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

        delogger.decorators.memory_profile._can_memory_profiler = _tmp

    def test_line_memory_profile_decorator(self, capsys, caplog):
        delogger = Delogger("line_memory_profile_decorator")
        delogger.load_modes(StreamDebugMode())
        delogger.load_decorators(LineMemoryProfile())
        logger = delogger.get_logger()

        @logger.line_memory_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret
