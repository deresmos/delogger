from logging import INFO
from typing import Optional

from delogger.handlers.slack import SlackHandler
from delogger.modes.base import ModeBase

__all__ = ["SlackWebhookMode", "SlackTokenMode"]


class SlackWebhookMode(ModeBase):
    def __init__(self, webhook_url: str, level: Optional[int] = INFO, **kwargs) -> None:
        super().__init__(**kwargs)

        self.webhook_url = webhook_url
        self.level = level

    def load(self, delogger) -> None:
        slack_hdlr = SlackHandler(url=self.webhook_url, as_user=True)
        delogger.add_handler(slack_hdlr, self.level, self.fmt, self.datefmt)


class SlackTokenMode(ModeBase):
    def __init__(
        self, token: str, channel: str, level: Optional[int] = INFO, **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.token = token
        self.channel = channel
        self.level = level

    def load(self, delogger) -> None:
        slack_hdlr = SlackHandler(token=self.token, channel=self.channel, as_user=True)
        delogger.add_handler(slack_hdlr, self.level, self.fmt, self.datefmt)
