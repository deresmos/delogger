from abc import ABC, abstractmethod
from logging import Logger
from os import getenv
from typing import Optional

from delogger import Delogger, DeloggerQueue
from delogger.logger.base import DeloggerBase
from delogger.mode.file import CountRotatingFileMode, TimedRotatingFileMode
from delogger.mode.slack import SlackWebhookMode


class PresetsBase(ABC):
    def __init__(self, name: str, is_queue: bool = False) -> None:
        self.name = getenv("DELOGGER_NAME") or name
        self.is_queue = is_queue

        self.filepath: Optional[str] = getenv("DELOGGER_FILEPATH")
        self.slack_webhook: Optional[str] = getenv("DELOGGER_SLACK_WEBHOOK")

    @abstractmethod
    def make_logger(self, delogger: DeloggerBase) -> Logger:
        pass

    def get_logger(self) -> Logger:
        _delogger = DeloggerQueue if self.is_queue else Delogger
        return self.make_logger(_delogger(self.name))

    def count_rorating_filemode(self) -> CountRotatingFileMode:
        return (
            CountRotatingFileMode(self.filepath)
            if self.filepath
            else CountRotatingFileMode()
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