import logging

from delogger import Delogger
from delogger.modes.base import PropagateMode
from tests.lib.base import Assert, DeloggerTestBase


class TestPropagateMode(DeloggerTestBase):
    def test_propagate_mode(self, capsys, caplog):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger()

        delogger = Delogger("propagate_mode", modes=[PropagateMode()])
        logger = delogger.get_logger()

        self.execute_log(logger)

        Assert._bool(caplog.record_tuples)

    def test_no_propagate(self, capsys, caplog):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger()

        delogger = Delogger("no_propagate_mode")
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_normal_stream_log(logger, capsys, is_color=True)
