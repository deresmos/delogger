from logging import WARNING

import requests
from tests.lib.base import DeloggerTestBase

from delogger import Delogger
from delogger.modes.slack import SlackWebhookMode


class TestSlackMode(DeloggerTestBase):
    def setup_class(self):
        self.requests_post = requests.post

    def teardown_class(self):
        requests.post = self.requests_post

    def setup_method(self):
        from unittest.mock import MagicMock

        requests.post = MagicMock()

    def test_slack_webhook_mode_info(self):
        delogger = Delogger("slack_webhook_mode_info")
        delogger.load_modes(SlackWebhookMode("http://dummy??"))
        logger = delogger.get_logger()

        self.execute_log(logger)

        assert requests.post.call_count == 4

    def test_slack_webhook_mode_warning(self):
        delogger = Delogger("slack_webhook_mode_warning")
        delogger.load_modes(SlackWebhookMode("http://dummy??", WARNING))
        logger = delogger.get_logger()

        self.execute_log(logger)

        assert requests.post.call_count == 3
