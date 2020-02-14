from os import getenv
from typing import Optional

from delogger.modes.file import RunRotatingFileMode, TimedRotatingFileMode
from delogger.modes.slack import SlackWebhookMode


class PresetsEnv:
    def __init__(self) -> None:
        self.filepath = getenv("DELOGGER_FILEPATH")
        self.slack_webhook = getenv("DELOGGER_SLACK_WEBHOOK")


class PresetsBase:
    def __init__(self) -> None:
        self.filepath: Optional[str] = getenv("DELOGGER_FILEPATH")
        self.slack_webhook: Optional[str] = getenv("DELOGGER_SLACK_WEBHOOK")

    def run_rorating_filemode(self) -> RunRotatingFileMode:
        return (
            RunRotatingFileMode(self.filepath)
            if self.filepath
            else RunRotatingFileMode()
        )

    def timed_rotating_filemode(self) -> TimedRotatingFileMode:
        return (
            TimedRotatingFileMode(self.filepath)
            if self.filepath
            else TimedRotatingFileMode()
        )

    def slack_webhook_mode(self) -> Optional[SlackWebhookMode]:
        slack_webhook = self.slack_webhook
        if slack_webhook:
            return SlackWebhookMode(slack_webhook)

        return None
