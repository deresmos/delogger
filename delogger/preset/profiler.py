from logging import Logger

from delogger.logger.base import DeloggerBase
from delogger.decorator.debug_log import DebugLog
from delogger.decorator.profiles import (
    LineMemoryProfile,
    LineProfile,
    LineProfileStats,
    MemoryProfile,
)
from delogger.mode.stream import StreamColorDebugMode
from delogger.preset.base import PresetsBase


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
