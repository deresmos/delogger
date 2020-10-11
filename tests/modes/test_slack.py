from logging import WARNING
import urllib.request

from delogger import Delogger
from delogger.modes.slack import SlackTokenMode
from delogger.modes.slack import SlackWebhookMode
from tests.lib.base import DeloggerTestBase


class TestSlackMode(DeloggerTestBase):
    def setup_class(self):
        self.urlopen = urllib.request.urlopen

    def teardown_class(self):
        urllib.request.urlopen = self.urlopen

    def setup_method(self):
        from unittest.mock import MagicMock

        urllib.request.urlopen = MagicMock()

    def test_slack_webhook_mode_info(self):
        delogger = Delogger("slack_webhook_mode_info")
        delogger.load_modes(SlackWebhookMode("http://dummy??"))
        logger = delogger.get_logger()

        self.execute_log(logger)

        assert urllib.request.urlopen.call_count == 4

    def test_slack_webhook_mode_warning(self):
        delogger = Delogger("slack_webhook_mode_warning")
        delogger.load_modes(SlackWebhookMode("http://dummy??", WARNING))
        logger = delogger.get_logger()

        self.execute_log(logger)

        assert urllib.request.urlopen.call_count == 3

    def test_slack_token_mode_info(self):
        delogger = Delogger("slack_mode_info")
        delogger.load_modes(SlackTokenMode("slack_token", "channel"))
        logger = delogger.get_logger()

        self.execute_log(logger)

        assert urllib.request.urlopen.call_count == 4
