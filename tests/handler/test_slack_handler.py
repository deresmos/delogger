import logging
import os

import pytest

from delogger.handler.slack import SlackHandler


class TestSlackHandler:
    def setup_class(self):
        self.dummy_url = "dummy.url"
        self.dummy_token = "dummy.token"
        self.debug_record = logging.LogRecord("name", logging.DEBUG, "", "", "", "", "")

    def test_normal(self):
        logger = logging.getLogger("normal")
        logger.setLevel(logging.DEBUG)

        slack_handler = SlackHandler(url=self.dummy_url, channel="#dummy")
        slack_handler.setLevel(logging.DEBUG)
        logger.addHandler(slack_handler)

        assert slack_handler.url != SlackHandler.POST_MESSAGE_URL
        assert "Authorization" not in slack_handler.headers

        logger.debug("normal test")

    def test_slack_handler_dup(self):
        logger = logging.getLogger("slack_dup")
        logger.setLevel(logging.DEBUG)

        slack_handler = SlackHandler(url=self.dummy_url, channel="#dummy")
        slack_handler.setLevel(logging.DEBUG)
        logger.addHandler(slack_handler)

        slack_handler = SlackHandler(url=self.dummy_url, channel="#dummy")
        slack_handler.setLevel(logging.DEBUG)
        logger.addHandler(slack_handler)

        assert slack_handler.url != SlackHandler.POST_MESSAGE_URL
        assert len(logger.handlers) == 1

        logger.debug("slack handler duplication")

    def test_url_env(self):
        url_env = SlackHandler.URL_ENV
        os.environ[url_env] = self.dummy_url

        SlackHandler(channel="#dummy")

    def test_url_env_error(self):
        url_env = SlackHandler.URL_ENV
        if os.environ.get(url_env, None):
            del os.environ[url_env]

        with pytest.raises(ValueError):
            SlackHandler(channel="#dummy")

    def test_token(self):
        logger = logging.getLogger("normal")
        logger.setLevel(logging.DEBUG)

        slack_handler = SlackHandler(token=self.dummy_token, channel="#dummy")

        assert slack_handler.url == SlackHandler.POST_MESSAGE_URL
        assert slack_handler.headers["Authorization"] == f"Bearer {self.dummy_token}"

    def test_token_env(self):
        token_env = SlackHandler.TOKEN_ENV
        os.environ[token_env] = self.dummy_token

        slack_handler = SlackHandler(channel="#dummy")

        assert slack_handler.url == SlackHandler.POST_MESSAGE_URL

    def test_token_error(self):
        url_env = SlackHandler.URL_ENV
        token_env = SlackHandler.TOKEN_ENV

        if os.environ.get(url_env, None):
            del os.environ[url_env]

        if os.environ.get(token_env, None):
            del os.environ[token_env]

        logger = logging.getLogger("error")
        logger.setLevel(logging.DEBUG)

        with pytest.raises(ValueError):
            SlackHandler()

        logger.debug("error test")

    def test_make_content_with_url(self):
        slack_handler = SlackHandler(url=self.dummy_url)
        content = slack_handler.make_json(self.debug_record)
        levelno = self.debug_record.levelno

        assert content["icon_emoji"] == slack_handler.emojis[levelno]
        assert content["username"] == slack_handler.usernames[levelno]
        assert "as_user" not in content

        assert slack_handler.url != SlackHandler.POST_MESSAGE_URL

    def test_make_content_with_token(self):
        slack_handler = SlackHandler(
            token=self.dummy_token, channel="#dummy", as_user=True
        )
        content = slack_handler.make_json(self.debug_record)

        assert "icon_emoji" not in content
        assert "username" not in content
        assert content["channel"] == "#dummy"
        assert content["as_user"]

        assert slack_handler.url == SlackHandler.POST_MESSAGE_URL

    def test_params(self):
        slack_handler = SlackHandler(
            url=self.dummy_url, emoji="emoji", username="username"
        )
        content = slack_handler.make_json(self.debug_record)

        assert content["icon_emoji"] == "emoji"
        assert content["username"] == "username"
