from logging import DEBUG

from delogger import DeloggerQueue
from delogger.handlers.run_rotating import RunRotatingHandler


def _set_logger():
    delogger = DeloggerQueue(name="output_only")
    delogger.default = False

    rrh = RunRotatingHandler("log", backup_count=-1, fmt="%Y-%m-%d.log")
    delogger.add_handler(rrh, DEBUG, fmt=delogger.file_fmt)

    return delogger.logger


logger = _set_logger()
