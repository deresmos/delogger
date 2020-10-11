from pathlib import Path
from shutil import rmtree

from delogger import Delogger
from delogger.modes.file import CountRotatingFileMode
from delogger.modes.file import TimedRotatingFileMode
from tests.lib.base import Assert
from tests.lib.base import DeloggerTestBase


class TestFileMode(DeloggerTestBase):
    def teardown_method(self):
        log_dir = self.OUTPUT_DIRPATH
        if not Path(log_dir).is_dir():
            return False
        rmtree(log_dir)

    def test_count_rotation_mode(self, capsys):
        count_rotation_mode = CountRotatingFileMode()
        delogger = Delogger("count_rotationg_file_mode")
        delogger.load_modes(count_rotation_mode)
        logger = delogger.get_logger()

        logfile = count_rotation_mode.logfile

        self.execute_log(logger)
        self.check_log_file(logfile.filepath)

        Assert._bool(logfile.filepath.exists())
        logfile.filepath.unlink()
        logfile.filepath.parent.rmdir()

    def test_count_rotation_filepath_mode(self, capsys):
        count_rotation_mode = CountRotatingFileMode(
            filepath=f"{self.OUTPUT_DIRPATH}/test.log"
        )
        delogger = Delogger("count_rotationg_file_filepath_mode")
        delogger.load_modes(count_rotation_mode)
        logger = delogger.get_logger()

        logfile = count_rotation_mode.logfile

        self.execute_log(logger)
        self.check_log_file(logfile.filepath)

        Assert._bool(logfile.filepath.exists())
        logfile.filepath.unlink()
        logfile.filepath.parent.rmdir()

    def test_timed_rotating_file_mode(self, capsys):
        timed_file_mode = TimedRotatingFileMode()
        delogger = Delogger("timed_rotating_file_mode")
        delogger.load_modes(timed_file_mode)
        logger = delogger.get_logger()

        logfile = timed_file_mode.logfile

        self.execute_log(logger)
        self.check_log_file(logfile.filepath)

        Assert._bool(logfile.filepath.exists())
        logfile.filepath.unlink()
        logfile.filepath.parent.rmdir()
