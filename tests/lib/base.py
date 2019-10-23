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


class DeloggerTestBase:
    DEBUG_FMT = r'[^\s]+\s? \[[^\s]+ File "[^\s]+", line \d{1,5}, in [^\s]+\] %s'
    INFO_FMT = r"%s"
    COLOR_FMT = (
        r"(\x1b\[\d{1,3}m)+\w+\s?\x1b\[0m "
        r'\[[^\s]+ File "[^\s]+", line \d{1,5}, in [^\s]+\] %s\x1b\[0m'
    )
    LOG_FMT = (
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} " r'[^\s]+\s? [^\s]+ [^\s]+ \d{1,5} "%s"'
    )

    def check_normal_stream_log(self, logger, capsys, is_color=False):
        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")

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
        # logger stream test
        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")

        captured = capsys.readouterr()

        fmt = self.COLOR_FMT if is_color else self.DEBUG_FMT
        streams = ["debug", "info", "warning", "error"]
        streams = [fmt % stream for stream in streams]
        logs = captured.err.split("\n")
        for stream, log in zip(streams, logs):
            Assert._match(stream, log)

    def check_log_file(self, logpath):
        logs = ["debug", "info", "warning", "error"]
        logs = [self.LOG_FMT % stream for stream in logs]

        for path in Path(logpath).iterdir():
            with open(str(path), "r") as f:
                for line, log in zip(f, logs):
                    Assert._match(log, line)
