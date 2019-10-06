import os

from delogger import Delogger


def _set_logger():
    delogger = Delogger("debug_logger")
    delogger.is_debug_stream = True
    delogger.is_color_stream = True
    delogger.is_save_file = True

    slack_hdlr = None
    if os.environ.get("DELOGGER_SLACK_URL", None):
        slack_hdlr = SlackHandler()
    elif os.environ.get("DELOGGER_SLACK_TOKEN", None):
        token = os.environ.get("DELOGGER_SLACK_TOKEN", None)
        channel = os.environ.get("DELOGGER_SLACK_CHANNEL")
        slack_hdlr = SlackHandler(token=token, channel=channel)

    if slack_hdlr:
        delogger.add_handler(slack_hdlr, INFO)

    return delogger.logger


logger = _set_logger()
