import pytest
from delogger.util.log_file import LogFile
from tests.lib.base import DeloggerTestBase


class TestLogFile(DeloggerTestBase):
    def test_eq(self):
        logfile = LogFile("log")

        with pytest.raises(NotImplementedError):
            if logfile == "no":
                pass

    def test_contains(self):
        logfile = LogFile("log")
        same_logfile = LogFile("log")

        assert same_logfile in logfile

    def test_str(self):
        logfile = LogFile("log")

        assert str(logfile) == "log"
