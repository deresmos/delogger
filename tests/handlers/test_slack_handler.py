import logging

import pytest

from delogger.handlers.slack import SlackHandler
from tests.lib.urlopen_mock import UrlopenMock


class TestSlackHandler:
    def setup_class(self):
        self.dummy_url = "http://dummy.url"
        self.dummy_token = "dummy.token"
        self.debug_record = logging.LogRecord("name", logging.DEBUG, "", "", "", "", "")

    def test_normal(self):
        urlopen_mock = UrlopenMock()

        logger = logging.getLogger("normal")
        logger.setLevel(logging.DEBUG)

        slack_handler = SlackHandler(url=self.dummy_url, channel="#dummy")
        slack_handler.setLevel(logging.DEBUG)
        logger.addHandler(slack_handler)

        assert slack_handler.url != SlackHandler.POST_MESSAGE_URL
        assert "Authorization" not in slack_handler.headers

        logger.debug("normal test")

        assert urlopen_mock.call_count == 1

    def test_slack_handler_dup(self):
        urlopen_mock = UrlopenMock()

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

        assert urlopen_mock.call_count == 1

    def test_token(self):
        logger = logging.getLogger("normal")
        logger.setLevel(logging.DEBUG)

        slack_handler = SlackHandler(token=self.dummy_token, channel="#dummy")

        assert slack_handler.url == SlackHandler.POST_MESSAGE_URL
        assert slack_handler.headers["Authorization"] == f"Bearer {self.dummy_token}"

    def test_token_error(self):
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

    def test_not_emit(self):
        urlopen_mock = UrlopenMock()

        logger = logging.getLogger("not_emit_to_slack")
        logger.setLevel(logging.DEBUG)

        slack_handler = SlackHandler(url=self.dummy_url, channel="#dummy")
        slack_handler.setLevel(logging.DEBUG)
        slack_handler.is_emit = False
        logger.addHandler(slack_handler)

        assert slack_handler.url != SlackHandler.POST_MESSAGE_URL
        assert "Authorization" not in slack_handler.headers

        logger.debug("normal test")

        urlopen_mock.assert_not_called()

    def test_eq(self):
        slack_handler = SlackHandler(url=self.dummy_url, channel="#dummy")

        with pytest.raises(NotImplementedError):
            if slack_handler == "11":
                pass

    def test_handle_error(self):
        urlopen_mock = UrlopenMock()
        urlopen_mock.load(side_effect=Exception())

        logger = logging.getLogger("slack_exception")
        logger.setLevel(logging.DEBUG)

        slack_handler = SlackHandler(url=self.dummy_url, channel="#dummy")
        slack_handler.setLevel(logging.DEBUG)
        logger.addHandler(slack_handler)

        logger.debug("normal test")

        assert urlopen_mock.call_count == 1
