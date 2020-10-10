from logging import Logger

from delogger import Delogger
from delogger.decorator.debug_log import DebugLog
from delogger.mode.stream import StreamColorDebugMode
from delogger.preset.base import PresetsBase


class DebugStreamPresets(PresetsBase):
    def make_logger(self, delogger: Delogger) -> Logger:
        delogger.load_modes(StreamColorDebugMode())
        delogger.load_decorators(DebugLog())

        return delogger.get_logger()


logger = DebugStreamPresets("debug_stream").get_logger()
