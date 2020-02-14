from logging import Logger

from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.decorators.profiles import (
    LineMemoryProfile,
    LineProfile,
    LineProfileStats,
    MemoryProfile,
)
from delogger.modes.stream import StreamColorDebugMode
from delogger.presets.base import PresetsBase


def _get_logger() -> Logger:
    run_rorating_filemode = PresetsBase().run_rorating_filemode()

    delogger = Delogger("profiler_logger")
    delogger.load_modes(StreamColorDebugMode(), run_rorating_filemode)
    delogger.load_decorators(
        DebugLog(),
        LineProfile(),
        LineProfileStats(),
        MemoryProfile(),
        LineMemoryProfile(),
    )

    return delogger.get_logger()


logger = _get_logger()
