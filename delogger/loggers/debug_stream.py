from ..logger import Delogger


def _set_logger():
    delogger = Delogger('debug_stream')
    delogger.is_debug_stream = True
    delogger.is_color_stream = True

    return delogger.logger


logger = _set_logger()
