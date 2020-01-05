import os
from logging import Logger

from delogger import DeloggerQueue
from delogger.decorators.debug_log import DebugLog
from delogger.modes.file import TimedRotatingFileMode


def _get_logger() -> Logger:
    delogger = DeloggerQueue("output_logger")
    delogger.load_modes(TimedRotatingFileMode())
    delogger.load_decorators(DebugLog())

    slack_webhook = os.getenv("DELOGGER_SLACK_WEBHOOK")
    if slack_webhook:
        from delogger.modes.slack import SlackWebhookMode

        delogger.load_modes(SlackWebhookMode(slack_webhook))

    return delogger.get_logger()


logger = _get_logger()
