from logging import Logger

from delogger.decorators.debug_log import DebugLog
from delogger.loggers.base import DeloggerBase
from delogger.modes.stream import StreamColorDebugMode
from delogger.presets.base import PresetsBase


class DebugPresets(PresetsBase):
    def make_logger(self, delogger: DeloggerBase) -> Logger:
        delogger.load_modes(StreamColorDebugMode(), self.count_rorating_filemode())
        delogger.load_decorators(DebugLog())

        return delogger.get_logger()


logger = DebugPresets("debug_logger").get_logger()
