from logging import Logger

from delogger.decorators.debug_log import DebugLog
from delogger.loggers.base import DeloggerBase
from delogger.modes.stream import StreamInfoMode
from delogger.presets.base import PresetsBase


class InfoPresets(PresetsBase):
    def make_logger(self, delogger: DeloggerBase) -> Logger:
        delogger.load_modes(StreamInfoMode())
        delogger.load_decorators(DebugLog())

        return delogger.get_logger()


logger = InfoPresets("info_logger").get_logger()
