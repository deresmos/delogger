import logging
import re
import shutil
from datetime import datetime as dt
from pathlib import Path

from delogger import Delogger
from tests.deprecated.config import (
    TODAY,
    _debug_stream_logger,
    _dp,
    _log_file,
    _normal_stream_logger,
)


def test_delogger_normal(capsys):
    delogger = Delogger()
    logger = delogger.logger

    _normal_stream_logger(logger, capsys)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_color(capsys):
    delogger = Delogger(name="color", is_color_stream=True, date_fmt="%H:%M:%S")
    logger = delogger.logger

    _normal_stream_logger(logger, capsys, is_color=True)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_color_debug(capsys):
    delogger = Delogger(
        name="color_debug",
        is_color_stream=True,
        is_debug_stream=True,
        date_fmt="%H:%M:%S",
    )
    logger = delogger.logger

    _debug_stream_logger(logger, capsys, is_color=True)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_debug(capsys):
    delogger = Delogger("debug", is_debug_stream=True)
    logger = delogger.logger

    _debug_stream_logger(logger, capsys)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_debug_instance(capsys):
    delogger = Delogger("debug_instance")
    delogger.is_debug_stream = True
    logger = delogger.logger

    _debug_stream_logger(logger, capsys)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_class_debug(capsys):
    Delogger.is_debug_stream = True

    try:
        delogger = Delogger("debug_class")
        logger = delogger.logger

        _debug_stream_logger(logger, capsys)

        captured = capsys.readouterr()

        streams = [
            (
                r"START test_delogger_class_debug.<locals>.test"
                r" args=\(\'test\', \'args\'\) kwargs={}"
            ),
            (
                r"END test_delogger_class_debug.<locals>.test"
                r" return=\(\'test\', \'args\'\)"
            ),
        ]
        streams = [_dp % stream for stream in streams]
        errors = captured.err.split("\n")[-3:-1]
        for err, stream in zip(errors, streams):
            assert re.findall(stream, err)

            assert not Path(delogger.dirpath).is_dir()

    finally:
        Delogger.is_debug_stream = False


def test_delogger_savelog(capsys):
    delogger = Delogger(name="savelog", is_save_file=True)
    logger = delogger.logger

    _normal_stream_logger(logger, capsys)

    logpath = delogger.dirpath
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)
    shutil.rmtree(delogger.dirpath)


def test_delogger_savelog_debug(capsys):
    delogger = Delogger(name="savelog_debug", is_save_file=True, is_debug_stream=True)
    logger = delogger.logger

    _debug_stream_logger(logger, capsys)

    logpath = delogger.dirpath
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)
    shutil.rmtree(delogger.dirpath)


def test_delogger_savelog_onefile(capsys):
    filename = "onefile.log"
    delogger = Delogger(name="savelog_onefile", is_save_file=True, filename=filename)
    logger = delogger.logger

    _normal_stream_logger(logger, capsys)

    logpath = delogger.dirpath
    assert (Path(logpath) / filename).exists()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)
    shutil.rmtree(delogger.dirpath)


def test_delogger_savelog_filepath(capsys):
    filepath = "./%Y/%dtest.log"
    delogger = Delogger(name="savelog_filepath", is_save_file=True, filepath=filepath)
    logger = delogger.logger
    _filepath = dt.strftime(TODAY, filepath)

    _normal_stream_logger(logger, capsys)

    assert Path(_filepath).exists()

    logdir = str(Path(_filepath).parent)
    _log_file(logdir)
    shutil.rmtree(logdir)


def test_delogger_savelog_filepath_nameonly(capsys):
    filepath = "%dtest.log"
    delogger = Delogger(
        name="savelog_filepath_name", is_save_file=True, filepath=filepath
    )
    logger = delogger.logger
    _filepath = dt.strftime(TODAY, filepath)

    _normal_stream_logger(logger, capsys)

    assert Path(_filepath).exists()

    Path(_filepath).unlink()


def test_delogger_is_stream(capsys):
    filename = "onefile.log"
    delogger = Delogger(
        name="disable_stream", is_save_file=True, filename=filename, is_stream=False
    )
    logger = delogger.logger

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")

    captured = capsys.readouterr()
    assert not captured.err

    logpath = delogger.dirpath
    assert (Path(logpath) / filename).exists()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)
    shutil.rmtree(delogger.dirpath)


def test_delogger_no_propagate(capsys, caplog):
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger()

    delogger = Delogger("propagate")
    logger = delogger.logger

    logger.info("OK")

    captured = capsys.readouterr()
    streams = ["OK"]
    errors = captured.err.split("\n")
    for err, stream in zip(errors, streams):
        assert re.findall(stream, err)

    # Check no propagate
    assert not caplog.records
