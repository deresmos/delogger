import datetime
import re
from pathlib import Path

TODAY = datetime.datetime.today()


class Assert:
    @staticmethod
    def _match(pattern: str, string: str) -> None:
        assert re.match(pattern, string)  # nosec

    @staticmethod
    def _bool(value: bool) -> None:
        assert value  # nosec


# YYYY-MM-DD hh:mm:ss.000
F_ASCTIME_L = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}"
# hh:mm:ss
F_ASCTIME_S = r"\d{2}:\d{2}:\d{2}"
F_LEVEL_NAME = r"(DEBUG|INFO|WARN|ERROR|CRIT)\s?"
F_FILENAME = r"[^\s]+"
F_LINENO = r"\d+"
F_COLOR_START = r"(\x1b\[\d{1,3}m)+"
F_COLOR_END = r"\x1b\[0m"
F_MESSAGE = r"%s"


class DeloggerTestBase:
    DEBUG_FMT = rf"{F_LEVEL_NAME} {F_ASCTIME_S} {F_FILENAME}:{F_LINENO} {F_MESSAGE}"
    INFO_FMT = r"{F_MESSAGE}"
    COLOR_FMT = (
        rf"{F_COLOR_START}{F_LEVEL_NAME}{F_COLOR_END} "
        rf"{F_ASCTIME_S} {F_FILENAME}:{F_LINENO} {F_MESSAGE}{F_COLOR_END}"
    )
    LOG_FMT = rf"{F_ASCTIME_L} {F_LEVEL_NAME} {F_FILENAME}:{F_LINENO} {F_MESSAGE}"

    ALL_LEVELS = ["debug", "info", "warning", "error", "critical"]

    def check_normal_stream_log(self, logger, capsys, is_color=False):
        captured = capsys.readouterr()
        if is_color:
            streams = [
                "info",
                self.COLOR_FMT % "warning",
                self.COLOR_FMT % "error",
                self.COLOR_FMT % "critical",
            ]
        else:
            streams = [
                "info",
                self.DEBUG_FMT % "warning",
                self.DEBUG_FMT % "error",
                self.DEBUG_FMT % "critical",
            ]
        logs = captured.err.split("\n")
        for stream, log in zip(streams, logs):
            Assert._match(stream, log)

    def check_debug_stream_log(self, logger, capsys, is_color=False):
        captured = capsys.readouterr()

        fmt = self.COLOR_FMT if is_color else self.DEBUG_FMT
        streams = self.ALL_LEVELS
        streams = [fmt % stream for stream in streams]
        logs = captured.err.split("\n")
        for stream, log in zip(streams, logs):
            Assert._match(stream, log)

    def check_log_file(self, filepath):
        logs = [self.LOG_FMT % stream for stream in self.ALL_LEVELS]

        _filepath = Path(filepath)
        if not _filepath.is_file():
            raise FileNotFoundError(_filepath)

        if _filepath.stat().st_size <= 0:
            raise Exception("Empty file")

        with open(str(filepath), "r") as f:
            for log, line in zip(logs, f):
                Assert._match(log, line)

    def execute_log(self, logger):
        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")
