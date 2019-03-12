from ..logger import Delogger


def _set_logger():
    delogger = Delogger('debug_logger')
    delogger.is_debug_stream = True
    delogger.is_color_stream = True
    delogger.is_save_file = True

    return delogger.logger


logger = _set_logger()
