from logging import Logger

from delogger.decorators.debug_log import DebugLog
from delogger.loggers.base import DeloggerBase
from delogger.modes.stream import StreamColorDebugMode
from delogger.presets.base import PresetsBase


class DebugStreamPresets(PresetsBase):
    def make_logger(self, delogger: DeloggerBase) -> Logger:
        delogger.load_modes(StreamColorDebugMode())
        delogger.load_decorators(DebugLog())

        return delogger.get_logger()


logger = DebugStreamPresets("debug_stream").get_logger()
