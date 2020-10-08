import datetime
import logging
import shutil
from pathlib import Path

from delogger.handlers.count_rotating_file import CountRotatingFileHandler
from tests.lib.base import DeloggerTestBase


class TestCountRotatingHandler(DeloggerTestBase):
    def setup_class(self):
        CountRotatingFileHandler._files = []
        self.today = datetime.datetime.today()
        self.logpath_set = set()

    def teardown_class(self):
        for path in reversed(sorted(self.logpath_set)):
            logpath = datetime.datetime.strftime(self.today, path)
            if Path(logpath).is_dir():
                shutil.rmtree(logpath)
            else:
                assert Path(logpath).is_dir()

    def _normal_logger(self, name, logpath):
        self.logpath_set.add(str(Path(logpath).parent))

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        count_rotating = CountRotatingFileHandler(logpath)
        count_rotating.setLevel(logging.DEBUG)
        logger.addHandler(count_rotating)

        return logger

    def _unlimit_logger(self, name, logpath):
        self.logpath_set.add(str(Path(logpath).parent))

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        count_rotating = CountRotatingFileHandler(logpath, backup_count=0)
        count_rotating.setLevel(logging.DEBUG)
        logger.addHandler(count_rotating)

        return logger

    def assert_normal(self, logpath, file_count):
        _logpath = Path(logpath)
        _logdir = _logpath.parent

        assert _logdir.is_dir()
        assert len(list(_logdir.glob("*.log"))) == file_count

    def test_normal(self):
        logpath = f"{self.OUTPUT_DIRPATH}/%Y%m%d_%H%M%S.log"
        logger = self._normal_logger("normal", logpath)

        logger.debug("log file test")
        self.assert_normal(logpath, 1)

    def test_same_filepath(self):
        logpath = f"{self.OUTPUT_DIRPATH}/%Y%m%d_%H%M%S.log"
        logger = self._normal_logger("same_filepath", logpath)

        logger.debug("same normal logger")
        self.assert_normal(logpath, 1)

    def test_same_dir(self):
        logpath = f"{self.OUTPUT_DIRPATH}/%Y%m%d_%H%M%S_new.log"
        logger = self._normal_logger("same_dir", logpath)

        logger.debug("same normal logger")
        self.assert_normal(logpath, 2)

    def test_another_dir(self):
        logpath = f"{self.OUTPUT_DIRPATH}/log/%Y.log"
        logger = self._normal_logger("another_dir", logpath)

        logger.debug("log file test")
        self.assert_normal(logpath, 1)

    def test_unlimit(self):
        logpath = f"{self.OUTPUT_DIRPATH}/%Y%m%d_%H%M%S%f_unlimit.log"
        logger = self._unlimit_logger("unlimit", logpath)

        logger.debug("log file test")
        self.assert_normal(logpath, 3)

    def test_unlimit_same_filepath(self):
        logpath = f"{self.OUTPUT_DIRPATH}/%Y%m%d_%H%M%S%f_unlimit.log"
        logger = self._unlimit_logger("unlimit_same_filepath", logpath)

        logger.debug("log file test")
        self.assert_normal(logpath, 3)

    def test_unlimit_same_dir(self):
        logpath = f"{self.OUTPUT_DIRPATH}/%Y%m%d_%H%M%S%f_unlimit_new.log"
        logger = self._unlimit_logger("unlimit_same_dir", logpath)

        logger.debug("log file test")
        self.assert_normal(logpath, 4)
