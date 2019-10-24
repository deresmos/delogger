from json import dumps as json_dumps
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Handler
from os import getenv

import requests


class SlackHandler(Handler):
    """Handler to send to Slack.

    Args:
        url (str): slack webhook url.
        channel (str): Slack channel to be transmitted.
        as_user (bool): Whether to send as a user.
        token (str): slack token.

        emoji (str): Emoji on sending.
        username (str): Username on sending.
        emojis (dict): Emojis on sending.
        usernames (dict): Usernames on sending.

    Attributes:
        url (str): slack webhook url.
        channel (str): Slack channel to be transmitted.
        as_user (bool): Whether to send as a user.
        token (str): slack token.

        emoji (str): Emoji on sending.
        username (str): Username on sending.
        emojis (dict): Emojis on sending.
        usernames (dict): Usernames on sending.

    """

    TIMEOUT = 20
    """default timeout for requests."""

    EMOJIS = {
        NOTSET: ":loudspeaker:",
        DEBUG: ":simple_smile:",
        INFO: ":smile:",
        WARNING: ":sweat:",
        ERROR: ":sob:",
        CRITICAL: ":scream:",
    }
    """Default value of emojis."""

    USERNAMES = {
        NOTSET: "Notset",
        DEBUG: "Debug",
        INFO: "Info",
        WARNING: "Warning",
        ERROR: "Erorr",
        CRITICAL: "Critical",
    }
    """Default value of usernames."""

    URL_ENV = "DELOGGER_SLACK_URL"
    """Environment variable name of slack webhook url."""

    TOKEN_ENV = "DELOGGER_TOKEN"
    """Environment variable name of slack token."""

    POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
    """Execution when using token API."""

    def __init__(
        self,
        url=None,
        channel=None,
        as_user=False,
        token=None,
        *,
        emoji=None,
        username=None,
        emojis=None,
        usernames=None
    ):
        self.is_emit = True

        self.url = url or getenv(self.URL_ENV)
        self.token = token or getenv(self.TOKEN_ENV)
        if self.token:
            self.url = self.POST_MESSAGE_URL

        if not self.url:
            self.is_emit = False
            raise ValueError("Not set url")

        self.token = token
        self.channel = channel
        self.usernames = usernames if token else self.USERNAMES
        self.emojis = emojis if token else self.EMOJIS
        self.as_user = as_user
        self.emoji = emoji
        self.username = username

        super().__init__()

    def _makeContent(self, levelno, content=None):
        """Get slack's payload."""

        content = content or {}

        if self.as_user:
            content["as_user"] = self.as_user

        else:
            if self.emoji:
                content["icon_emoji"] = self.emoji
            elif self.emojis:
                content["icon_emoji"] = self.emojis[levelno]

            if self.username:
                content["username"] = self.username
            elif self.usernames:
                content["username"] = self.usernames[levelno]

        if self.channel:
            content["channel"] = self.channel

        if self.token:
            content["token"] = self.token
        else:
            content = json_dumps(content)

        return content

    def makeContent(self, record):
        """Get slack's payload."""

        content = {"text": self.format(record)}
        content = self._makeContent(record.levelno, content=content)

        return content

    def emit(self, record):
        """Send a message to Slack."""

        try:
            if not self.is_emit:
                return

            requests.post(self.url, data=self.makeContent(record), timeout=self.TIMEOUT)

        except Exception:
            self.handleError(record)

    def __eq__(self, other):
        """Comparison for SlackHandler.

        Returns:
            True if token, url, level and channel is the same, False otherwise.

        """

        if not isinstance(other, SlackHandler):
            if isinstance(other, Handler):
                return False

            raise NotImplementedError

        eq = False
        if (
            other.token == self.token
            and other.url == self.url
            and other.level == self.level
            and other.channel == self.channel
        ):
            eq = True

        return eq

    def __hash__(self):
        return hash("{}{}{}{}".format(self.token, self.url, self.level, self.channel))
