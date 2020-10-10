import logging

from delogger.logger.base import DeloggerBase
from tests.lib.base import DeloggerTestBase


class TestDeloggerBase(DeloggerTestBase):
    def test_only_filter(self, capsys):
        delogger = DeloggerBase("only_filter")
        delogger.add_stream_handler(
            logging.INFO, hdlr=logging.StreamHandler(), only_level=True
        )

        logger = delogger.get_logger()

        logger.debug("no")
        logger.info("only")

        expected_logs = [
            "only",
        ]
        self.check_capsys(capsys, expected_logs)

    def test_only_filter_again(self, capsys):
        delogger = DeloggerBase("only_filter_again")
        delogger.add_stream_handler(
            logging.INFO, hdlr=logging.StreamHandler(), only_level=True
        )
        logger = delogger.get_logger()

        logger.debug("no")
        logger.info("only")

        expected_logs = [
            "only",
        ]
        self.check_capsys(capsys, expected_logs)

        delogger = DeloggerBase("only_filter_again")
        logger = delogger.get_logger()

        logger.debug("no")
        logger.info("only")

        expected_logs = [
            "only",
        ]
        self.check_capsys(capsys, expected_logs)
