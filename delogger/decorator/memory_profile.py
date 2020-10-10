from delogger.decorator.base import DecoratorBase
from delogger.util.warn import warn_import

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

    def can_run(self) -> bool:
        try:
            profile
        except NameError:
            warn_import(self.decorator_name, "memory_profiler")
            return False

        return True

    def wrapper(self, f, *args, **kwargs):
        # output memory_profiler
        with StringIO() as s:
            rtn = profile(f, stream=s, precision=2)(*args, **kwargs)
            msg = "memory_profiler result\n{}".format(s.getvalue())
        self.logger.debug(msg)

        return rtn
