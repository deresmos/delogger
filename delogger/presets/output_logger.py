import os
from logging import INFO

from delogger import DeloggerQueue
from delogger.handlers.slack import SlackHandler
from delogger.modes.file import TimedRotatingFileMode


def _get_logger():
    delogger = DeloggerQueue("debug_logger")
    delogger.load_modes(TimedRotatingFileMode())

    slack_webhook = os.getenv("DELOGGER_SLACK_WEBHOOK")
    if slack_webhook:
        slack_hdlr = SlackHandler(url=slack_webhook, as_user=True)
        delogger.add_handler(slack_hdlr, INFO)

    return delogger.get_logger()


logger = _get_logger()
