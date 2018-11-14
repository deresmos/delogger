import atexit
from copy import copy
from logging import (CRITICAL, DEBUG, INFO, WARNING, Formatter, StreamHandler,
                     addLevelName, getLogger)
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

from colorlog import ColoredFormatter

from delogger import OnlyFilter, RunRotatingHandler


class DeloggerSetting(object):
    date_fmt = '%Y-%m-%d %H:%M:%S'
    stream_level = INFO
    file_level = DEBUG
    save_log = False
    color_log = False
    debug_mode = False
    default = True
    log_dir = 'log'

    file_fmt = ('%(asctime)s %(levelname)-5s %(name)s %(filename)s '
                '%(lineno)d "%(message)s"')

    stream_fmts = [
        '%(message)s',
        ('%(asctime)s %(levelname)s %(filename)s %(name)s '
         '%(lineno)s "%(message)s"'),
    ]
    stream_color_fmts = [
        '%(log_color)s%(levelname)-5s%(reset)s %(message)s',
        '%(log_color)s%(levelname)-5s%(reset)s %(message)s',
    ]

    FMT_INFO = 0
    FMT_DEBUG = 1

    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARN': 'yellow',
        'ERROR': 'red',
        'CRIT': 'red,bg_white',
    }

    def __init__(self,
                 save_log=None,
                 logdir=None,
                 debug_mode=None,
                 color_log=None,
                 stream_level=None,
                 file_level=None,
                 date_fmt=None,
                 default=None):
        self.init_attr('save_log', save_log)
        self.init_attr('log_dir', logdir)
        self.init_attr('debug_mode', debug_mode)
        self.init_attr('color_log', color_log)
        self.init_attr('stream_level', stream_level)
        self.init_attr('file_level', file_level)
        self.init_attr('dete_fmt', date_fmt)
        self.init_attr('default', default)

        addLevelName(WARNING, 'WARN')
        addLevelName(CRITICAL, 'CRIT')

    def init_attr(self, key, value):
        if value is None:
            # class variable
            pass
        else:
            # instance variable
            setattr(self, key, value)

    @property
    def stream_fmt(self):
        if self.debug_mode:
            index = self.FMT_DEBUG
            self.stream_level = DEBUG
        else:
            index = self.FMT_INFO
        fmts = self.stream_color_fmts if self.color_log else self.stream_fmts

        fmt = fmts[index]

        return fmt


class Delogger(DeloggerSetting):
    def __init__(self, name=None, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        name_ = parent or self
        name_ = name or type(name_).__name__
        logger = getLogger(name_)
        self._logger = logger

        if len(self._logger.handlers) > 0:
            # Already set logger
            self._is_new_logger = False
        else:
            # Not set logger
            self._is_new_logger = True

    @property
    def logger(self):
        if self._is_new_logger and self.default:
            self.default_logger()
            self._is_new_logger = False

        return self._logger

    @classmethod
    def debuglog(cls, func):
        logger = cls(name='_debugger').logger

        def wrapper(*args, **kwargs):
            msg = 'START {} args={} kwargs={}'.format(
                func.__qualname__,
                args,
                kwargs,
            )
            logger.debug(msg)

            rtn = func(*args, **kwargs)
            msg = 'END {} return={}'.format(
                func.__qualname__,
                rtn,
            )
            logger.debug(msg)

            return rtn

        return wrapper

    def default_logger(self):
        self._logger.setLevel(DEBUG)

        fmt = self.stream_fmt
        self.add_stream_handler(
            self.stream_level, fmt=fmt, color_log=self.color_log)

        if self.save_log:
            rrh = RunRotatingHandler(self.log_dir)
            self.add_handler(rrh, DEBUG, fmt=self.file_fmt)

    def add_handler(self,
                    hdlr,
                    level,
                    fmt=None,
                    datefmt=None,
                    only_level=False,
                    formatter=None):
        hdlr.setLevel(level)

        datefmt = datefmt or self.date_fmt
        formatter = formatter or Formatter(fmt, datefmt)
        hdlr.setFormatter(formatter)

        if only_level:
            hdlr.addFilter(OnlyFilter(level))

        self._logger.addHandler(hdlr)

    def add_stream_handler(self,
                           level,
                           *,
                           check_level=False,
                           color_log=False,
                           hdlr=None,
                           **kwargs):
        if check_level and self.stream_level <= level:
            return

        if color_log:
            fmt = ColoredFormatter(
                kwargs.get('fmt', None),
                log_colors=self.log_colors,
                style='%',
            )
            kwargs.setdefault('formatter', fmt)

        hdlr = hdlr or StreamHandler()
        self.add_handler(hdlr, level, **kwargs)


class DeloggerQueue(Delogger):
    _que = None
    _listener = None

    def __init__(self, default=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = default

    def default_logger(self):
        if not DeloggerQueue._listener:
            super().default_logger()

        self.queue_logger()

    def queue_logger(self):
        if DeloggerQueue._listener:
            queue_handler = QueueHandler(DeloggerQueue._que)
            self._logger.addHandler(queue_handler)

        else:
            # init que and listener
            handlers = copy(self._logger.handlers)
            for hdlr in handlers:
                self._logger.removeHandler(hdlr)

            que = Queue(-1)
            queue_handler = QueueHandler(que)
            listener = QueueListener(
                que, *handlers, respect_handler_level=True)
            self._logger.addHandler(queue_handler)
            listener.start()

            DeloggerQueue._que = que
            DeloggerQueue._listener = listener

            atexit.register(self.listener_stop)

    def listener_stop(self):
        if DeloggerQueue._listener:
            DeloggerQueue._listener.stop()
