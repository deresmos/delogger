import logging
import os

from delogger.loggers.base import DeloggerBase
from tests.lib.base import DeloggerTestBase


class TestDeloggerBase(DeloggerTestBase):
    def test_delogger_base(self, capsys):
        delogger = DeloggerBase()
        delogger.add_stream_handler(
            logging.INFO, hdlr=logging.StreamHandler(), only_level=True
        )

        logger = delogger.get_logger()

        logger.debug("no")
        logger.info("only")

        expected_logs = [
            "no",
            "only",
        ]
        self.check_capsys(capsys, expected_logs)

        assert logger.name == "delogger"

    def test_logger_name(self, capsys):
        os.environ["DELOGGER_NAME"] = "logger"
        delogger = DeloggerBase()
        delogger.add_stream_handler(
            logging.INFO, hdlr=logging.StreamHandler(), only_level=True
        )
        del os.environ["DELOGGER_NAME"]

        logger = delogger.get_logger()

        logger.debug("no")
        logger.info("only")

        expected_logs = [
            "no",
            "only",
        ]
        self.check_capsys(capsys, expected_logs)

        assert logger.name == "logger"

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
