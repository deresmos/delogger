import shutil
from pathlib import Path

from .config import TODAY, _debug_stream_logger, _dp, _log_file, _normal_stream_logger


def test_debug_logger(capsys):
    from delogger.loggers.debug_logger import logger

    _debug_stream_logger(logger, capsys, is_color=True)
    _log_file("log")

    assert Path("log").is_dir()
    shutil.rmtree("log")


def test_debug_stream(capsys):
    from delogger.loggers.debug_stream import logger

    _debug_stream_logger(logger, capsys, is_color=True)

    assert not Path("log").is_dir()


def test_output_only(capsys):
    from delogger.loggers.output_only import logger

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")

    _log_file("log")

    assert Path("log").is_dir()
    shutil.rmtree("log")
