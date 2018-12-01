import re
import shutil
from pathlib import Path

from delogger import Delogger

_dp = (r'[^\s]+\s? \[[^\s]+ File "[^\s]+", line \d{1,5}, in [^\s]+\] %s')
_cp = r'\x1b\[\d{1,3}m\w+\s?\x1b\[0m %s\x1b\[0m'
_cdp = (r'\x1b\[\d{1,3}m\w+\s?\x1b\[0m '
        r'\[[^\s]+ File "[^\s]+", line \d{1,5}, in [^\s]+\] %s\x1b\[0m')
_lp = (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} '
       r'[^\s]+\s? [^\s]+ [^\s]+ \d{1,5} "%s"')


def _normal_stream_logger(logger, capsys, is_color=False):
    # logger stream test
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')

    captured = capsys.readouterr()
    if is_color:
        streams = [_cp % 'info', _cdp % 'warning', _cdp % 'error']
    else:
        streams = ['info', _dp % 'warning', _dp % 'error']
    errors = captured.err.split('\n')
    for err, stream in zip(errors, streams):
        assert re.findall(stream, err)


def _debug_stream_logger(logger, capsys, is_color=False):
    # logger stream test
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    captured = capsys.readouterr()

    _p = _cdp if is_color else _dp
    streams = ['debug', 'info', 'warning', 'error']
    streams = [_p % stream for stream in streams]
    errors = captured.err.split('\n')
    for err, stream in zip(errors, streams):
        assert re.findall(stream, err)


def _log_file(logpath):
    logs = ['debug', 'info', 'warning', 'error']
    logs = [_lp % stream for stream in logs]

    for path in Path(logpath).iterdir():
        with open(str(path), 'r') as f:
            for line, log in zip(f, logs):
                assert re.findall(log, line)


def test_delogger_normal(capsys):
    delogger = Delogger()
    logger = delogger.logger

    @Delogger.debuglog
    def test(*args):
        return args

    test('test', 'args')

    _normal_stream_logger(logger, capsys)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_color(capsys):
    delogger = Delogger(name='color', is_color_stream=True)
    logger = delogger.logger

    _normal_stream_logger(logger, capsys, is_color=True)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_color_debug(capsys):
    delogger = Delogger(
        name='color_debug', is_color_stream=True, is_debug_stream=True)
    logger = delogger.logger

    _debug_stream_logger(logger, capsys, is_color=True)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_debug(capsys):
    delogger = Delogger('debug', is_debug_stream=True)
    logger = delogger.logger

    @Delogger.debuglog
    def test(*args):
        return args

    test('test', 'args')

    _debug_stream_logger(logger, capsys)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_class_debug(capsys):
    Delogger.is_debug_stream = True

    try:
        delogger = Delogger('debug_class')
        logger = delogger.logger

        _debug_stream_logger(logger, capsys)

        @Delogger.debuglog
        def test(*args):
            return args

        test('test', 'args')

        captured = capsys.readouterr()

        streams = [(r'START test_delogger_class_debug.<locals>.test'
                    r' args=\(\'test\', \'args\'\) kwargs={}'),
                   (r'END test_delogger_class_debug.<locals>.test'
                    r' return=\(\'test\', \'args\'\)')]
        streams = [_dp % stream for stream in streams]
        errors = captured.err.split('\n')[-3:-1]
        for err, stream in zip(errors, streams):
            assert re.findall(stream, err)

            assert not Path(delogger.dirpath).is_dir()

    finally:
        Delogger.is_debug_stream = False


def test_delogger_savelog(capsys):
    delogger = Delogger(name='savelog', is_save_file=True)
    logger = delogger.logger

    _normal_stream_logger(logger, capsys)

    logpath = delogger.dirpath
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)
    shutil.rmtree(delogger.dirpath)


def test_delogger_savelog_debug(capsys):
    delogger = Delogger(
        name='savelog_debug', is_save_file=True, is_debug_stream=True)
    logger = delogger.logger

    _debug_stream_logger(logger, capsys)

    logpath = delogger.dirpath
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)
    shutil.rmtree(delogger.dirpath)


def test_delogger_savelog_onefile(capsys):
    filename = 'onefile.log'
    delogger = Delogger(
        name='savelog_onefile', is_save_file=True, filename=filename)
    logger = delogger.logger

    _normal_stream_logger(logger, capsys)

    logpath = delogger.dirpath
    assert (Path(logpath) / filename).exists()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)
    shutil.rmtree(delogger.dirpath)
