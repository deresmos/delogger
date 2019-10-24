from pathlib import Path
from shutil import rmtree

from delogger import Delogger
from delogger.modes.file import RunRotatingMode
from tests.lib.base import Assert, DeloggerTestBase


class TestFileMode(DeloggerTestBase):
    LOG_DIR_LIST = ["log"]

    def teardown_method(self):
        for log_dir in self.LOG_DIR_LIST:
            if not Path(log_dir).is_dir():
                continue
            rmtree(log_dir)

    def test_run_rotation_mode(self, capsys):
        run_rotation_mode = RunRotatingMode()
        delogger = Delogger("file_run_rotationg_mode", modes=[run_rotation_mode])
        logger = delogger.get_logger()

        logfile = run_rotation_mode.logfile

        self.execute_log(logger)
        self.check_log_file(logfile.filepath)

        Assert._bool(logfile.filepath.exists())
        logfile.filepath.unlink()
        logfile.dirpath.rmdir()

    def test_run_rotation_filepath_mode(self, capsys):
        run_rotation_mode = RunRotatingMode(filepath="log/test.log")
        delogger = Delogger(
            "file_run_rotationg_filepath_mode", modes=[run_rotation_mode]
        )
        logger = delogger.get_logger()

        logfile = run_rotation_mode.logfile

        self.execute_log(logger)
        self.check_log_file(logfile.filepath)

        Assert._bool(logfile.filepath.exists())
        logfile.filepath.unlink()
        logfile.dirpath.rmdir()
