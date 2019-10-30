from pathlib import Path
from shutil import rmtree

from delogger import Delogger
from delogger.modes.file import RunRotatingFileMode, TimedRotatingFileMode
from tests.lib.base import Assert, DeloggerTestBase


class TestFileMode(DeloggerTestBase):
    LOG_DIR_LIST = ["log"]

    def teardown_method(self):
        for log_dir in self.LOG_DIR_LIST:
            if not Path(log_dir).is_dir():
                continue
            rmtree(log_dir)

    def test_run_rotation_mode(self, capsys):
        run_rotation_mode = RunRotatingFileMode()
        delogger = Delogger("file_run_rotationg_mode")
        delogger.load_modes(run_rotation_mode)
        logger = delogger.get_logger()

        logfile = run_rotation_mode.logfile

        self.execute_log(logger)
        self.check_log_file(logfile.filepath)

        Assert._bool(logfile.filepath.exists())
        logfile.filepath.unlink()
        logfile.dirpath.rmdir()

    def test_run_rotation_filepath_mode(self, capsys):
        run_rotation_mode = RunRotatingFileMode(filepath="log/test.log")
        delogger = Delogger("file_run_rotationg_filepath_mode")
        delogger.load_modes(run_rotation_mode)
        logger = delogger.get_logger()

        logfile = run_rotation_mode.logfile

        self.execute_log(logger)
        self.check_log_file(logfile.filepath)

        Assert._bool(logfile.filepath.exists())
        logfile.filepath.unlink()
        logfile.dirpath.rmdir()

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
        logfile.dirpath.rmdir()
