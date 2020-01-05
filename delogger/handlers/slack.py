from json import dumps as json_dumps
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Handler
from os import getenv
from typing import Any, Dict, Optional


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

    TIMEOUT: int = 20
    """default timeout for requests."""

    EMOJIS: Dict[int, str] = {
        NOTSET: ":loudspeaker:",
        DEBUG: ":simple_smile:",
        INFO: ":smile:",
        WARNING: ":sweat:",
        ERROR: ":sob:",
        CRITICAL: ":scream:",
    }
    """Default value of emojis."""

    USERNAMES: Dict[int, str] = {
        NOTSET: "Notset",
        DEBUG: "Debug",
        INFO: "Info",
        WARNING: "Warning",
        ERROR: "Erorr",
        CRITICAL: "Critical",
    }
    """Default value of usernames."""

    URL_ENV: str = "DELOGGER_SLACK_URL"
    """Environment variable name of slack webhook url."""

    TOKEN_ENV: str = "DELOGGER_TOKEN"
    """Environment variable name of slack token."""

    POST_MESSAGE_URL: str = "https://slack.com/api/chat.postMessage"
    """Execution when using token API."""

    def __init__(
        self,
        url: Optional[str] = None,
        channel: Optional[str] = None,
        as_user: bool = False,
        token: Optional[str] = None,
        *,
        emoji: Optional[str] = None,
        username: Optional[str] = None,
        emojis: Optional[Dict[int, str]] = None,
        usernames: Optional[Dict[int, str]] = None
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

    def _makeContent(
        self, levelno: int, content: Optional[Dict[str, Any]] = None
    ) -> str:
        """Get slack's payload."""

        _content: Dict[str, Any] = content or {}

        if self.as_user:
            _content["as_user"] = self.as_user

        else:
            if self.emoji:
                _content["icon_emoji"] = self.emoji
            elif self.emojis:
                _content["icon_emoji"] = self.emojis[levelno]

            if self.username:
                _content["username"] = self.username
            elif self.usernames:
                _content["username"] = self.usernames[levelno]

        if self.channel:
            _content["channel"] = self.channel

        if self.token:
            _content["token"] = self.token
        else:
            content_str = json_dumps(_content)

        return content_str

    def makeContent(self, record) -> str:
        """Get slack's payload."""

        content = {"text": self.format(record)}
        content_str = self._makeContent(record.levelno, content=content)

        return content_str

    def emit(self, record):
        """Send a message to Slack."""

        try:
            # TODO: temporary
            import requests

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
