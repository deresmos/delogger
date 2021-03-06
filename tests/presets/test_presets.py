import os
from pathlib import Path
from shutil import rmtree

from tests.lib.base import DeloggerTestBase
from tests.lib.urlopen_mock import UrlopenMock


class TestPresets(DeloggerTestBase):
    def teardown_method(self):
        log_dir = self.OUTPUT_DIRPATH
        if not Path(log_dir).is_dir():
            return False
        rmtree(log_dir)

    def test_info(self, capsys):
        from delogger.presets.info import logger

        self.execute_log(logger)

        self.check_normal_stream_log(logger, capsys, is_color=True)

        assert getattr(logger, "debuglog")

    def test_debug(self, capsys):
        from delogger.presets.debug import logger

        self.execute_log(logger)

        self.check_debug_stream_log(logger, capsys, is_color=True)

        run_rotating_hdlr = logger.handlers[1]
        self.check_log_file(run_rotating_hdlr.filepath)

        assert getattr(logger, "debuglog")

    def test_debug_stream(self, capsys):
        from delogger.presets.debug_stream import logger

        self.execute_log(logger)

        self.check_debug_stream_log(logger, capsys, is_color=True)

        assert getattr(logger, "debuglog")

    def test_output(self, capsys):
        from delogger.presets.output import logger

        self.execute_log(logger)

        assert getattr(logger, "debuglog")
        assert Path(self.OUTPUT_DIRPATH).is_dir()

    def test_output_env(self, capsys):
        urlopen_mock = UrlopenMock()

        filepath = f"{self.OUTPUT_DIRPATH}/test_output.log"
        os.environ["DELOGGER_NAME"] = "test_output_env"
        os.environ["DELOGGER_FILEPATH"] = filepath
        os.environ["DELOGGER_SLACK_WEBHOOK"] = "http://slack_webhook"
        from delogger.presets.output import OutputPresets

        logger = OutputPresets("no_name").get_logger()

        del os.environ["DELOGGER_NAME"]
        del os.environ["DELOGGER_FILEPATH"]
        del os.environ["DELOGGER_SLACK_WEBHOOK"]

        self.execute_log(logger)

        assert getattr(logger, "debuglog")
        assert Path(filepath).is_file()
        assert urlopen_mock.call_count == 4

    def test_profiler(self):
        from delogger.presets.profiler import logger

        self.execute_log(logger)

        assert getattr(logger, "debuglog")
        assert getattr(logger, "line_profile")
        assert getattr(logger, "add_line_profile")
        assert getattr(logger, "memory_profile")
        assert getattr(logger, "line_memory_profile")
