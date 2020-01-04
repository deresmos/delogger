import re
from datetime import datetime as dt
from pathlib import Path

_dp = r"\w+\s? \d{2}:\d{2}:\d{2} [^\s]+:\d{1,5} %s\x1b\[0m"
_cp = r"%s"
_cdp = r"(\x1b\[\d{1,3}m)+\w+\s?\x1b\[0m \d{2}:\d{2}:\d{2} [^\s]+:\d{1,5} %s\x1b\[0m"
_lp = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3} [^\s]+\s? [^\s]+:\d{1,5} %s"

TODAY = dt.today()


def _normal_stream_logger(logger, capsys, is_color=False):
    # logger stream test
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")

    captured = capsys.readouterr()
    if is_color:
        streams = [_cp % "info", _cdp % "warning", _cdp % "error"]
    else:
        streams = ["info", _dp % "warning", _dp % "error"]
    errors = captured.err.split("\n")
    for err, stream in zip(errors, streams):
        assert re.findall(stream, err)


def _debug_stream_logger(logger, capsys, is_color=False):
    # logger stream test
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    captured = capsys.readouterr()

    _p = _cdp if is_color else _dp
    streams = ["debug", "info", "warning", "error"]
    streams = [_p % stream for stream in streams]
    errors = captured.err.split("\n")
    for err, stream in zip(errors, streams):
        assert re.findall(stream, err)


def _log_file(logpath):
    logs = ["debug", "info", "warning", "error"]
    logs = [_lp % stream for stream in logs]

    for path in Path(logpath).iterdir():
        with open(str(path), "r") as f:
            for line, log in zip(f, logs):
                assert re.findall(log, line)
