from typing import Callable

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
        """When this decorator is set, the argument and return value are out-
        put to the log.
        """
        logger = self.logger

        def wrapper(*args, **kwargs):
            prof = LineProfiler()
            prof.add_function(func)

            rtn = prof.runcall(func, *args, **kwargs)
            with StringIO() as f:
                prof.print_stats(stream=f)
                msg = "line_profiler result\n{}".format(f.getvalue())
            logger.debug(msg)

            return rtn

        return wrapper
