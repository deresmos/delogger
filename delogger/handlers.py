import os
from datetime import datetime as dt
from json import dumps as json_dumps
from logging import (CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING,
                     FileHandler, Handler)
from os import getenv
from pathlib import Path

import requests


class _FILE_PATH(object):
    def __init__(self, dirname, basename):
        self.dirname = dirname
        self.basename = basename
        self.path = dt.today().strftime(str(Path(dirname) / basename))

    def __eq__(self, other):
        if not isinstance(other, _FILE_PATH):
            raise NotImplementedError
        eq = False
        eq = other.dirname == self.dirname

        return eq

    def __contains__(self, other):
        return other == self

    def __str__(self):
        return self.path


class RunRotatingHandler(FileHandler):
    LOG_FMT = '%Y%m%d_%H%M%S.log'
    BACKUP_COUNT = 5

    _files = []

    def __init__(self, dirname, backup_count=None, fmt=None, **kwargs):
        fmt = fmt or self.LOG_FMT
        backup_count = backup_count or self.BACKUP_COUNT

        self.filepath = self._load_file_path(dirname, fmt, backup_count)

        super().__init__(self.filepath, **kwargs)

    def _open(self):
        path_parent = Path(self.filepath).parent
        if not path_parent.is_dir():
            os.makedirs(str(path_parent))

        return super()._open()

    def _load_file_path(self, dirname, fmt, backup_count):
        # Set the logfile name
        path = _FILE_PATH(dirname, fmt)
        filepath = Path(str(path))

        # If already same dirname, return the filepath
        for fpath in RunRotatingHandler._files:
            if fpath == path:
                return str(fpath)

        # Get file list matching format
        filenames = sorted(filepath.parent.glob('*'))

        # Delete the old file and set a new file path
        if len(filenames) >= backup_count:
            os.remove(filenames[0])

        RunRotatingHandler._files.append(path)
        return str(path)


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

    def __init__(self,
                 url=None,
                 channel=None,
                 as_user=False,
                 token=None,
                 *,
                 emoji=None,
                 username=None,
                 emojis=None,
                 usernames=None):
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
