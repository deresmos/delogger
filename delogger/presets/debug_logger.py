from delogger import Delogger
from delogger.modes.file import RunRotatingFileMode
from delogger.modes.stream import ColorStremDebugMode


def _get_logger():
    delogger = Delogger("debug_logger")
    delogger.load_modes(ColorStremDebugMode(), RunRotatingFileMode())

    return delogger.get_logger()


logger = _get_logger()
