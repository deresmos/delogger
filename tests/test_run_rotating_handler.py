import logging
import shutil
from datetime import datetime as dt
from pathlib import Path

from delogger import RunRotatingHandler

_log_paths = []
TODAY = dt.today()


def test_start():
    RunRotatingHandler._files = []


def _normal_logger(name, logpath):
    _log_paths.append(logpath)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    runrotating = RunRotatingHandler(logpath)
    runrotating.setLevel(logging.DEBUG)
    logger.addHandler(runrotating)

    return logger


def test_normal():
    logpath = 'log'
    logger = _normal_logger('normal', logpath)

    logger.debug('log file test')
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1
    assert len(RunRotatingHandler._files) == len(_log_paths)


def test_normal_same():
    logpath = 'log'
    logger = logging.getLogger('normal')

    logger.debug('same normal logger')
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1
    assert len(RunRotatingHandler._files) == len(_log_paths)


def test_normal2():
    logpath = 'log2'
    logger = _normal_logger('normal2', logpath)

    logger.debug('log file test')
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1
    assert len(RunRotatingHandler._files) == len(_log_paths)


def test_logpath():
    logpath = 'log/logs'
    logger = _normal_logger('logpath', logpath)

    logger.debug('log path test: %s', logpath)
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1
    assert len(RunRotatingHandler._files) == len(_log_paths)


def test_logpath2():
    logpath = 'log/%Y/%M'
    logger = _normal_logger('logpath2', logpath)
    logpath = dt.strftime(TODAY, logpath)

    logger.debug('log path test: %s', logpath)
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1
    assert len(RunRotatingHandler._files) == len(_log_paths)


def test_end():
    for path in reversed(sorted(_log_paths)):
        logpath = dt.strftime(TODAY, path)
        if Path(logpath).is_dir():
            shutil.rmtree(logpath)
        else:
            assert Path(logpath).is_dir()
