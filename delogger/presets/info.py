from logging import Logger

from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.modes.stream import StreamInfoMode
from delogger.presets.base import PresetsBase


class InfoPresets(PresetsBase):
    def make_logger(self, delogger: Delogger) -> Logger:
        delogger.load_modes(StreamInfoMode())
        delogger.load_decorators(DebugLog())

        return delogger.get_logger()


logger = InfoPresets("info_logger").get_logger()
