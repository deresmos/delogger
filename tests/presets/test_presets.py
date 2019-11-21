from pathlib import Path
from shutil import rmtree

from delogger import Delogger
from tests.lib.base import Assert, DeloggerTestBase


class TestPresets(DeloggerTestBase):
    LOG_DIR_LIST = ["log"]

    def teardown_method(self):
        for log_dir in self.LOG_DIR_LIST:
            if not Path(log_dir).is_dir():
                continue
            rmtree(log_dir)

    def test_debug(self, capsys):
        from delogger.presets.debug import logger

        self.execute_log(logger)

        self.check_debug_stream_log(logger, capsys, is_color=True)

        run_rotating_hdlr = logger.handlers[1]
        self.check_log_file(run_rotating_hdlr.filepath)

        assert getattr(logger, "debuglog")
