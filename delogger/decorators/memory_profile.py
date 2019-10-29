from typing import Callable

from delogger.decorators.base import DecoratorBase

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from memory_profiler import profile
except ImportError:
    pass


class MemoryProfile(DecoratorBase):
    decorator_name = "memory_profile"

    def decorator(self, func) -> Callable:
        """When this decorator is set, the argument and return value are out-
        put to the log.
        """
        logger = self.logger

        def wrapper(*args, **kwargs):
            # output memory_profiler
            with StringIO() as f:
                rtn = profile(func, stream=f, precision=2)(*args, **kwargs)
                msg = "memory_profiler result\n{}".format(f.getvalue())
            logger.debug(msg)

            return rtn

        return wrapper