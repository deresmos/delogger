from logging import Logger

from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.modes.stream import StreamInfoMode


def _get_logger() -> Logger:
    delogger = Delogger("debug_logger")
    delogger.load_modes(StreamInfoMode())
    delogger.load_decorators(DebugLog())

    return delogger.get_logger()


logger = _get_logger()
