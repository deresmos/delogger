import logging

from delogger import Delogger
from delogger.modes.propagete import NotPropagateMode
from delogger.modes.stream import StreamInfoMode
from tests.lib.base import Assert
from tests.lib.base import DeloggerTestBase


class TestPropagateMode(DeloggerTestBase):
    def test_propagate_mode(self, capsys, caplog):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger()

        delogger = Delogger("propagate_mode")
        delogger.load_modes()
        logger = delogger.get_logger()

        self.execute_log(logger)

        Assert._bool(caplog.record_tuples)
        assert delogger.propagate is True

    def test_not_propagate(self, capsys, caplog):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger()

        delogger = Delogger("not_propagate_mode")
        delogger.load_modes(StreamInfoMode(), NotPropagateMode())
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_normal_stream_log(logger, capsys, is_color=False)

    def test_not_propagate_setter(self, capsys, caplog):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger()

        delogger = Delogger("not_propagate_mode_setter")
        delogger.propagate = False
        delogger.load_modes(StreamInfoMode())
        logger = delogger.get_logger()

        self.execute_log(logger)
        self.check_normal_stream_log(logger, capsys, is_color=False)
        assert delogger.propagate is False
