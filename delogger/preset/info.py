from logging import Logger

from delogger.decorator.debug_log import DebugLog
from delogger.logger.base import DeloggerBase
from delogger.mode.stream import StreamInfoMode
from delogger.preset.base import PresetsBase


class InfoPresets(PresetsBase):
    def make_logger(self, delogger: DeloggerBase) -> Logger:
        delogger.load_modes(StreamInfoMode())
        delogger.load_decorators(DebugLog())

        return delogger.get_logger()


logger = InfoPresets("info_logger").get_logger()
