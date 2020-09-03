from logging import Logger

from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.modes.stream import StreamColorDebugMode
from delogger.presets.base import PresetsBase


def _get_logger() -> Logger:
    count_rorating_filemode = PresetsBase().count_rorating_filemode()
    delogger = Delogger("debug_logger")
    delogger.load_modes(StreamColorDebugMode(), count_rorating_filemode)
    delogger.load_decorators(DebugLog())

    return delogger.get_logger()


logger = _get_logger()
