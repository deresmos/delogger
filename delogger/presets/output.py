from logging import Logger

from delogger import DeloggerQueue
from delogger.decorators.debug_log import DebugLog
from delogger.presets.base import PresetsBase


def _get_logger() -> Logger:
    presets_base = PresetsBase()
    timed_rotating_filemode = presets_base.timed_rotating_filemode()

    delogger = DeloggerQueue("output_logger")
    delogger.load_modes(timed_rotating_filemode)
    delogger.load_decorators(DebugLog())

    slack_webhook_mode = presets_base.slack_webhook_mode()
    if slack_webhook_mode:
        delogger.load_modes(slack_webhook_mode)

    return delogger.get_logger()


logger = _get_logger()
