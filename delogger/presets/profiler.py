from logging import Logger

from delogger.decorators.debug_log import DebugLog
from delogger.decorators.profiles import LineMemoryProfile
from delogger.decorators.profiles import LineProfile
from delogger.decorators.profiles import LineProfileStats
from delogger.decorators.profiles import MemoryProfile
from delogger.loggers.base import DeloggerBase
from delogger.modes.stream import StreamColorDebugMode
from delogger.presets.base import PresetsBase


class ProfilerPresets(PresetsBase):
    def make_logger(self, delogger: DeloggerBase) -> Logger:
        delogger.load_modes(StreamColorDebugMode(), self.count_rorating_filemode())
        delogger.load_decorators(
            DebugLog(),
            LineProfile(),
            LineProfileStats(),
            MemoryProfile(),
            LineMemoryProfile(),
        )

        return delogger.get_logger()


logger = ProfilerPresets("profiler_logger").get_logger()
