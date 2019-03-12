from ..handlers import RunRotatingHandler
from ..logger import DeloggerQueue


def _set_logger():
    delogger = DeloggerQueue(name='output_only')
    delogger.default = False

    rrh = RunRotatingHandler('log', backup_count=-1, fmt='%Y-%m-%d.log')
    delogger.add_handler(rrh, delogger.DEBUG, fmt=delogger.file_fmt)

    return delogger.logger


logger = _set_logger()
