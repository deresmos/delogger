import datetime
import logging
import shutil
from pathlib import Path

from delogger.handlers.count_rotating_file import CountRotatingFileHandler


class TestRunRotatingHandler:
    def setup_class(self):
        CountRotatingFileHandler._files = []
        self.today = datetime.datetime.today()
        self.log_paths = []

    def teardown_class(self):
        for path in reversed(sorted(self.log_paths)):
            logpath = datetime.datetime.strftime(self.today, path)
            if Path(logpath).is_dir():
                shutil.rmtree(logpath)
            else:
                assert Path(logpath).is_dir()

    def _normal_logger(self, name, logpath):
        self.log_paths.append(logpath)

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        runrotating = CountRotatingFileHandler(logpath)
        runrotating.setLevel(logging.DEBUG)
        logger.addHandler(runrotating)

        return logger

    def _filepath_logger(self, name, logpath):
        self.log_paths.append(str(Path(logpath).parent))

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        runrotating = CountRotatingFileHandler(filepath=logpath)
        runrotating.setLevel(logging.DEBUG)
        logger.addHandler(runrotating)

        return logger

    def test_normal(self):
        logpath = "log"
        logger = self._normal_logger("normal", logpath)

        logger.debug("log file test")
        assert Path(logpath).is_dir()
        assert len(list(Path(logpath).iterdir())) == 1
        assert len(CountRotatingFileHandler._files) == len(self.log_paths)

    def test_normal_same(self):
        logpath = "log"
        logger = logging.getLogger("normal")

        logger.debug("same normal logger")
        assert Path(logpath).is_dir()
        assert len(list(Path(logpath).iterdir())) == 1
        assert len(CountRotatingFileHandler._files) == len(self.log_paths)

    def test_normal2(self):
        logpath = "log2"
        logger = self._normal_logger("normal2", logpath)

        logger.debug("log file test")
        assert Path(logpath).is_dir()
        assert len(list(Path(logpath).iterdir())) == 1
        assert len(CountRotatingFileHandler._files) == len(self.log_paths)

    def test_logpath(self):
        logpath = "log/logs"
        logger = self._normal_logger("logpath", logpath)

        logger.debug("log path test: %s", logpath)
        assert Path(logpath).is_dir()
        assert len(list(Path(logpath).iterdir())) == 1
        assert len(CountRotatingFileHandler._files) == len(self.log_paths)

    def test_logpath2(self):
        logpath = "log/%Y/%M"
        logger = self._normal_logger("logpath2", logpath)
        logpath = datetime.datetime.strftime(self.today, logpath)

        logger.debug("log path test: %s", logpath)
        assert Path(logpath).is_dir()
        assert len(list(Path(logpath).iterdir())) == 1
        assert len(CountRotatingFileHandler._files) == len(self.log_paths)

    def test_filepath(self):
        logpath = "log/%Y/%M%d/%Y.log"
        logger = self._normal_logger("filepath", logpath)
        logpath = datetime.datetime.strftime(self.today, logpath)

        logger.debug("log path test: %s", logpath)
        assert Path(logpath).parent.is_dir()
        assert len(list(Path(logpath).iterdir())) == 1
        assert Path(logpath).exists()
        assert len(CountRotatingFileHandler._files) == len(self.log_paths)
