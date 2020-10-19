from typing import Optional

from delogger.decorators.base import DecoratorBase
from delogger.util.warn import warn_import

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from line_profiler import LineProfiler

    _can_line_profiler = True
except ImportError:  # pragma: no cover
    _can_line_profiler = False


class LineProfile(DecoratorBase):
    decorator_name = "line_profile"

    def can_run(self) -> bool:
        if not _can_line_profiler:
            warn_import(self.decorator_name, "line_profiler")
            return False

        return True

    def wrapper(self, f, *args, **kwargs):
        prof = LineProfiler()
        prof.add_function(f)

        rtn = prof.runcall(f, *args, **kwargs)
        with StringIO() as f:
            prof.print_stats(stream=f)
            msg = "line_profiler result\n{}".format(f.getvalue())
            self.logger.debug(msg)

        return rtn


class LineProfileStats(DecoratorBase):
    decorator_name = "add_line_profile"

    def __init__(self) -> None:
        super().__init__()

        self.prof: Optional[LineProfiler] = None
        if _can_line_profiler:
            self.prof = LineProfiler()

    def can_run(self) -> bool:
        if not _can_line_profiler:
            warn_import(self.decorator_name, "line_profiler")
            return False

        return True

    def wrapper(self, f, *args, **kwargs):
        self.prof.add_function(f)

        rtn = self.prof.runcall(f, *args, **kwargs)

        return rtn

    def print_stats(self) -> None:
        if not self.prof:
            return None

        with StringIO() as f:
            self.prof.print_stats(stream=f)
            msg = "line_profiler_stats result\n{}".format(f.getvalue())
            self.logger.debug(msg)

    def load(self, delogger) -> None:
        super().load(delogger)

        setattr(delogger._logger, "print_stats", self.print_stats)
