from delogger import Delogger
import delogger.decorators.line_memory_profile
import delogger.decorators.line_profile
import delogger.decorators.memory_profile
from delogger.decorators.profiles import LineMemoryProfile
from delogger.decorators.profiles import LineProfile
from delogger.decorators.profiles import LineProfileStats
from delogger.decorators.profiles import MemoryProfile
from delogger.modes.stream import StreamDebugMode
from tests.lib.base import DeloggerTestBase
from tests.lib.line_profiler_mock import LineProfilerMock


class TestProfileDecorator(DeloggerTestBase):
    def test_line_profile_decorator(self):
        mock = LineProfilerMock()

        _delogger = Delogger("line_profile_decorator")
        _delogger.load_modes(StreamDebugMode())
        _delogger.load_decorators(LineProfile())
        logger = _delogger.get_logger()

        mock.assert_not_called()

        @logger.line_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

        mock.assert_called_once()
        mock.add_function.assert_called_once()
        mock.runcall.assert_called_once()
        mock.print_stats.assert_called_once()

    def test_line_profile_decorator_no_module(self):
        delogger.decorators.line_profile._can_line_profiler = False

        mock = LineProfilerMock()

        _delogger = Delogger("line_profile_decorator_no_module")
        _delogger.load_modes(StreamDebugMode())
        _delogger.load_decorators(LineProfile())
        logger = _delogger.get_logger()

        mock.assert_not_called()

        @logger.line_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

        mock.assert_not_called()
        mock.add_function.assert_not_called()
        mock.runcall.assert_not_called()
        mock.print_stats.assert_not_called()

        delogger.decorators.line_profile._can_line_profiler = True

    def test_line_profile_stats_decorator(self, capsys, caplog):
        mock = LineProfilerMock()

        _delogger = Delogger("line_profile_stats_decorator")
        _delogger.load_modes(StreamDebugMode())
        _delogger.load_decorators(LineProfileStats())
        logger = _delogger.get_logger()

        mock.assert_called_once()

        @logger.add_line_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

        mock.assert_called_once()
        mock.add_function.assert_called_once()
        mock.runcall.assert_called_once()
        mock.print_stats.assert_not_called()

        logger.print_stats()

        mock.print_stats.assert_called_once()

    def test_line_profile_stats_decorator_no_module(self, capsys, caplog):
        delogger.decorators.line_profile._can_line_profiler = False
        mock = LineProfilerMock()

        _delogger = Delogger("line_profile_stats_decorator_no_module")
        _delogger.load_modes(StreamDebugMode())
        _delogger.load_decorators(LineProfileStats())
        logger = _delogger.get_logger()

        mock.assert_not_called()

        @logger.add_line_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

        mock.assert_not_called()
        mock.add_function.assert_not_called()
        mock.runcall.assert_not_called()
        mock.print_stats.assert_not_called()

        logger.print_stats()

        mock.print_stats.assert_not_called()

        delogger.decorators.line_profile._can_line_profiler = True

    def test_memory_profile_decorator(self, capsys, caplog):
        _delogger = Delogger("memory_profile_decorator")
        _delogger.load_modes(StreamDebugMode())
        _delogger.load_decorators(MemoryProfile())
        logger = _delogger.get_logger()

        @logger.memory_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

    def test_memory_profile_decorator_no_module(self, capsys, caplog):
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

        delogger.decorators.memory_profile._can_memory_profiler = True

    def test_line_memory_profile_decorator_no_module(self, capsys, caplog):
        delogger.decorators.line_memory_profile._can_line_profiler = False
        delogger.decorators.line_memory_profile._can_memory_profiler = False

        mock = LineProfilerMock()

        _delogger = Delogger("line_memory_profile_decorator")
        _delogger.load_modes(StreamDebugMode())
        _delogger.load_decorators(LineMemoryProfile())
        logger = _delogger.get_logger()

        @logger.line_memory_profile
        def test_func(arg1, arg2=None):
            return True

        # Only execute
        ret = test_func("testarg", 123)
        assert ret

        delogger.decorators.line_memory_profile._can_line_profiler = True
        delogger.decorators.line_memory_profile._can_memory_profiler = True
