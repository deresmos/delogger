from json import dumps as json_dumps
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Handler
from os import getenv

import requests


class SlackHandler(Handler):
    TIMEOUT = 20

    EMOJIS = {
        NOTSET: ':loudspeaker:',
        DEBUG: ':simple_smile:',
        INFO: ':smile:',
        WARNING: ':sweat:',
        ERROR: ':sob:',
        CRITICAL: ':scream:'
    }

    USERNAMES = {
        NOTSET: 'Notset',
        DEBUG: 'Debug',
        INFO: 'Info',
        WARNING: 'Warning',
        ERROR: 'Erorr',
        CRITICAL: 'Critical',
    }

    URL_ENV = 'DELOGGER_SLACK_URL'
    TOKEN_ENV = 'DELOGGER_TOKEN'

    POST_MESSAGE_URL = 'https://slack.com/api/chat.postMessage'

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
            usernames=None,
    ):
        super().__init__()
        self.is_emit = True

        self.url = url or getenv(self.URL_ENV)
        self.token = token or getenv(self.TOKEN_ENV)
        if self.token:
            self.url = self.POST_MESSAGE_URL

        if not self.url:
            self.is_emit = False
            raise ValueError('Not set url')

        self.token = token
        self.channel = channel
        self.usernames = usernames if token else self.USERNAMES
        self.emojis = emojis if token else self.EMOJIS
        self.as_user = as_user
        self.emoji = emoji
        self.username = username

    def _makeContent(self, levelno):
        content = {}

        if self.emoji:
            content['icon_emoji'] = self.emoji
        elif self.emojis:
            content['icon_emoji'] = self.emojis[levelno]

        if self.username:
            content['username'] = self.username
        elif self.usernames:
            content['username'] = self.usernames[levelno]

        if self.channel:
            content['channel'] = self.channel

        if self.as_user:
            content['as_user'] = self.as_user

        if self.token:
            content['token'] = self.token
        else:
            content = json_dumps(content)

        return content

    def makeContent(self, record):
        content = {
            'text': self.format(record),
        }
        content.update(self._makeContent(record.levelno))

        return content

    def emit(self, record):
        try:
            if not self.is_emit:
                return

            requests.post(
                self.url,
                data=self.makeContent(record),
                timeout=self.TIMEOUT,
            )

        except Exception:
            self.handleError(record)
