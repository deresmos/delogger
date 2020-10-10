import json
import urllib.request
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
        usernames: Optional[Dict[int, str]] = None,
    ):
        self.is_emit = True

        self.url = url or getenv(self.URL_ENV)
        token = token or getenv(self.TOKEN_ENV)
        if token:
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

        self.headers = {"Content-Type": "application/json; charset=utf-8"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

        super().__init__()

    def make_json(self, record) -> Dict[str, Any]:
        json_data: Dict[str, Any] = {}

        json_data["text"] = self.format(record)
        if self.as_user:
            json_data["as_user"] = self.as_user

        else:
            if self.emoji:
                json_data["icon_emoji"] = self.emoji
            elif self.emojis:
                json_data["icon_emoji"] = self.emojis[record.levelno]

            if self.username:
                json_data["username"] = self.username
            elif self.usernames:
                json_data["username"] = self.usernames[record.levelno]

        if self.channel:
            json_data["channel"] = self.channel

        return json_data

    def make_payload(self, record) -> bytes:
        """Get slack's payload."""

        json_data = self.make_json(record)

        return json.dumps(json_data).encode("utf-8")

    def emit(self, record):
        """Send a message to Slack."""

        try:
            if not self.is_emit:
                return

            payload = self.make_payload(record)
            request = urllib.request.Request(
                url=self.url, method="POST", data=payload, headers=self.headers
            )
            urllib.request.urlopen(request, timeout=self.TIMEOUT)

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
