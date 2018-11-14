import re
from pathlib import Path

from delogger import Delogger

_dp = (r'[^\s]+\s? \[[^\s]+ [^\s]+ [^\s]+ \d{1,5}\] %s')
_cp = r'\x1b\[\d{1,3}m\w+\s?\x1b\[0m %s\x1b\[0m'
_lp = (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} '
       r'[^\s]+\s? [^\s]+ [^\s]+ \d{1,5} "%s"')


def _normal_stream_logger(logger, capsys):
    # logger stream test
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')

    captured = capsys.readouterr()
    streams = ['info', _dp % 'warning', _dp % 'error']
    errors = captured.err.split('\n')
    for err, stream in zip(errors, streams):
        assert re.findall(stream, err)


def _debug_stream_logger(logger, capsys):
    # logger stream test
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    captured = capsys.readouterr()

    streams = ['debug', 'info', 'warning', 'error']
    streams = [_dp % stream for stream in streams]
    errors = captured.err.split('\n')
    for err, stream in zip(errors, streams):
        assert re.findall(stream, err)


def _color_stream_logger(logger, capsys):
    # logger stream test
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    captured = capsys.readouterr()

    streams = ['info', 'warning', 'error']
    streams = [_cp % stream for stream in streams]
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
    delogger = Delogger(name='color', color=True)
    logger = delogger.logger

    _color_stream_logger(logger, capsys)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_debug(capsys):
    delogger = Delogger('debug', debug_mode=True)
    logger = delogger.logger

    @Delogger.debuglog
    def test(*args):
        return args

    test('test', 'args')

    _debug_stream_logger(logger, capsys)

    assert not Path(delogger.dirpath).is_dir()


def test_delogger_class_debug(capsys):
    Delogger.debug_mode = True

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
        Delogger.debug_mode = False


def test_delogger_savelog(capsys):
    delogger = Delogger(name='savelog', save=True)
    logger = delogger.logger

    _normal_stream_logger(logger, capsys)

    logpath = delogger.dirpath
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)


def test_delogger_savelog_debug(capsys):
    delogger = Delogger(name='savelog_debug', save=True, debug_mode=True)
    logger = delogger.logger

    _debug_stream_logger(logger, capsys)

    logpath = delogger.dirpath
    assert Path(logpath).is_dir()
    assert len(list(Path(logpath).iterdir())) == 1

    _log_file(logpath)
