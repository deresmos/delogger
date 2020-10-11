from logging import Logger

from delogger.decorator.debug_log import DebugLog
from delogger.logger.base import DeloggerBase
from delogger.mode.stream import StreamColorDebugMode
from delogger.preset.base import PresetsBase


class DebugPresets(PresetsBase):
    def make_logger(self, delogger: DeloggerBase) -> Logger:
        delogger.load_modes(StreamColorDebugMode(), self.count_rorating_filemode())
        delogger.load_decorators(DebugLog())

        return delogger.get_logger()


logger = DebugPresets("debug_logger").get_logger()
