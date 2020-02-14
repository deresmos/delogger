from logging import Logger

from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.decorators.profiles import (
    LineMemoryProfile,
    LineProfile,
    LineProfileStats,
    MemoryProfile,
)
from delogger.modes.file import RunRotatingFileMode
from delogger.modes.stream import StreamColorDebugMode


def _get_logger() -> Logger:
    delogger = Delogger("profiler_logger")
    delogger.load_modes(StreamColorDebugMode(), RunRotatingFileMode())
    delogger.load_decorators(
        DebugLog(),
        LineProfile(),
        LineProfileStats(),
        MemoryProfile(),
        LineMemoryProfile(),
    )

    return delogger.get_logger()


logger = _get_logger()
