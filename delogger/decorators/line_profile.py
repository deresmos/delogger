from typing import Callable, Optional

from delogger.decorators.base import DecoratorBase

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from line_profiler import LineProfiler
except ImportError:
    pass


class LineProfile(DecoratorBase):
    decorator_name = "line_profile"

    def decorator(self, func) -> Callable:
        def wrapper(*args, **kwargs):
            prof = LineProfiler()
            prof.add_function(func)

            rtn = prof.runcall(func, *args, **kwargs)
            with StringIO() as f:
                prof.print_stats(stream=f)
                msg = "line_profiler result\n{}".format(f.getvalue())
                self.logger.debug(msg)

            return rtn

        return wrapper


class LineProfileStats(DecoratorBase):
    decorator_name = "add_line_profile"

    def __init__(self) -> None:
        super().__init__()

        self.prof: Optional[LineProfiler] = None
        try:
            self.prof = LineProfiler()
        except NameError:
            pass

    def decorator(self, func) -> Callable:
        def wrapper(*args, **kwargs):
            if not self.prof:
                return func(*args, **kwargs)

            self.prof.add_function(func)

            rtn = self.prof.runcall(func, *args, **kwargs)

            return rtn

        return wrapper

    def print_stats(self) -> None:
        if not self.prof or not self.logger:
            return None

        with StringIO() as f:
            self.prof.print_stats(stream=f)
            msg = "line_profiler_stats result\n{}".format(f.getvalue())
            self.logger.debug(msg)

    def load_to_delogger(self, delogger) -> None:
        super().load_to_delogger(delogger)

        setattr(delogger._logger, "print_stats", self.print_stats)
