import os
import re
from datetime import datetime as dt
from json import dumps as json_dumps
from logging import (CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING,
                     FileHandler, Handler)
from os import getenv
from pathlib import Path

import requests


class _LOG_FILE(object):
    """Set the path of the log file.

    Args:
        dirname (str): Directory path.
        basename (str): Filename like date_string.

    Attributes:
        dirname (str): Directory path.
        basename (str): Filename like date_string.
        path (str): Log file path.

    """

    def __init__(self, dirname, basename):
        self.dirname = dirname
        self.basename = basename
        self.path = dt.today().strftime(str(Path(dirname) / basename))

    def __eq__(self, other):
        """Comparison for RunRotatingHandler.

        Returns:
            True if dirname is the same, False otherwise.

        """
        if not isinstance(other, _LOG_FILE):
            raise NotImplementedError
        eq = False
        eq = (other.dirname == self.dirname) \
            and (other.basename == self.basename)

        return eq

    def __contains__(self, other):
        return other == self

    def __str__(self):
        return self.path


class RunRotatingHandler(FileHandler):
    """This handler leaves a log file for each execution.

    Args:
        dirname (str): Directory path.
        backup_count (int): Leave logs up to the designated generation.
        fmt (str): Filename like date_string.

    Attributes:
        filepath (str): File path determined only once at runtime.

    """

    LOG_FMT = '%Y%m%d_%H%M%S.log'
    """Default value of log format."""

    BACKUP_COUNT = 5
    """Default value of backup count."""

    _files = []
    """This list saving _LOG_FILE of output log file."""

    _LOG_FMT_RE = {
        r'\d{4}': ['%Y'],
        r'\d{2}': ['%m', '%d', '%H', '%M', '%S'],
    }

    def __init__(self, dirname, backup_count=None, fmt=None, **kwargs):
        fmt = fmt or self.LOG_FMT
        backup_count = backup_count or self.BACKUP_COUNT

        self.filepath = self._load_file_path(dirname, fmt, backup_count)

        super().__init__(self.filepath, **kwargs)

    def _open(self):
        """It is executed at log output.

        If there is no directory, it will be created automatically.

        """

        # If there is no save destination directory, the directory is created.
        path_parent = Path(self.filepath).parent
        if not path_parent.is_dir():
            os.makedirs(str(path_parent))

        return super()._open()

    def _load_file_path(self, dirname, fmt, backup_count):
        """Get the file path of the log output destination.

        For each directory, determine the log file path only once at runtime.

        Args:
            dirname (str): Directory path.
            fmt (str): Filename like date_string.
            backup_count (int): Leave logs up to the designated generation.

        """

        # Set the logfile name.
        path = _LOG_FILE(dirname, fmt)
        filepath = Path(str(path))

        # If already same dirname, return the filepath.
        for fpath in RunRotatingHandler._files:
            if fpath == path:
                return str(fpath)

        # Get a file list that matches the format of fmt.
        filenames = self._get_match_files(filepath.parent, fmt)

        # Delete the old file and set a new file path
        if len(filenames) >= backup_count:
            os.remove(filenames[0])
        RunRotatingHandler._files.append(path)

        return str(path)

    def _get_match_files(self, dirpath, fmt):
        fmt_ = fmt
        for patter, date_strs in self._LOG_FMT_RE.items():
            for date_str in date_strs:
                fmt_ = fmt_.replace(date_str, patter)

        repa = re.compile(fmt_)
        files = [
            x for x in sorted(Path(dirpath).glob('*')) if repa.search(str(x))
        ]

        return files


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
        NOTSET: ':loudspeaker:',
        DEBUG: ':simple_smile:',
        INFO: ':smile:',
        WARNING: ':sweat:',
        ERROR: ':sob:',
        CRITICAL: ':scream:'
    }
    """Default value of emojis."""

    USERNAMES = {
        NOTSET: 'Notset',
        DEBUG: 'Debug',
        INFO: 'Info',
        WARNING: 'Warning',
        ERROR: 'Erorr',
        CRITICAL: 'Critical',
    }
    """Default value of usernames."""

    URL_ENV = 'DELOGGER_SLACK_URL'
    """Environment variable name of slack webhook url."""

    TOKEN_ENV = 'DELOGGER_TOKEN'
    """Environment variable name of slack token."""

    POST_MESSAGE_URL = 'https://slack.com/api/chat.postMessage'
    """Execution when using token API."""

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

    def _makeContent(self, levelno, content=None):
        """Get slack's payload."""

        content = content or {}

        if self.as_user:
            content['as_user'] = self.as_user

        else:
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

        if self.token:
            content['token'] = self.token
        else:
            content = json_dumps(content)

        return content

    def makeContent(self, record):
        """Get slack's payload."""

        content = {
            'text': self.format(record),
        }
        content = self._makeContent(record.levelno, content=content)

        return content

    def emit(self, record):
        """Send a message to Slack."""

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
        if other.token == self.token \
                and other.url == self.url \
                and other.level == self.level \
                and other.channel == self.channel:
            eq = True

        return eq
