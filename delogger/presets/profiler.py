from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.decorators.profiles import LineMemoryProfile, LineProfile, MemoryProfile
from delogger.modes.file import RunRotatingFileMode
from delogger.modes.stream import ColorStremDebugMode


def _get_logger():
    delogger = Delogger("profiler_logger")
    delogger.load_modes(ColorStremDebugMode(), RunRotatingFileMode())
    delogger.load_decorators(
        DebugLog(), LineProfile(), MemoryProfile(), LineMemoryProfile()
    )

    return delogger.get_logger()


logger = _get_logger()
