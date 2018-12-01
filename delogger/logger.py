import atexit
from copy import copy
from logging import (CRITICAL, DEBUG, ERROR, INFO, WARNING, Formatter,
                     StreamHandler, addLevelName, getLogger)
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

from colorlog import ColoredFormatter
from delogger import OnlyFilter, RunRotatingHandler


class DeloggerSetting(object):
    """Common configuration class of Delogger.

    Args:
        is_save_file (bool): Whether to save the log file.
        logdir (str): Log file save destination.
        is_debug_stream (bool): Whether to output a debug stream.
        is_color_stream (bool): Whether to output color stream.
        stream_level (int): Stream logger level.
        file_level (int): File logger level.
        date_fmt (str): Datetime format to be output.
        default (bool): Whether to use the default handler.

    Attributes:
        dirname (str): Directory path.
        basename (str): Filename like date_string.
        path (str): Log file path.

    """

    date_fmt = '%Y-%m-%d %H:%M:%S'
    """Default value of datetime format."""

    stream_level = INFO
    """Default value of stream logger level."""

    file_level = DEBUG
    """Default value of file logger level."""

    is_save_file = False
    """Default value of save file flag."""

    is_color_stream = False
    """Default value of color stream flag."""

    is_debug_stream = False
    """Default value of debug stream flag."""

    default = True
    """Default value of default logger."""

    dirpath = 'log'
    """Default value of log output destination directory."""

    backup_count = 5
    """Default value of RunRotatingHandler backup count."""

    filename = None
    """Default value of RunRotatingHandler filename (fmt)."""

    file_fmt = ('%(asctime)s %(levelname)-5s %(name)s %(filename)s '
                '%(lineno)d "%(message)s"')
    """Default value of file logger fmt."""

    stream_fmts = [
        '%(message)s',
        ('%(levelname)-5s [%(name)s File "%(filename)s", '
         'line %(lineno)d, in %(funcName)s] %(message)s'),
    ]
    """Default value of stream logger fmt.(0: normal, 1: debug)"""

    stream_color_fmts = [
        '%(log_color)s%(levelname)-5s%(reset)s %(message)s',
        ('%(log_color)s%(levelname)-5s%(reset)s [%(name)s '
         'File "%(filename)s", line %(lineno)d, in %(funcName)s] %(message)s'),
    ]
    """Default value of color stream logger fmt.(0: normal, 1: debug)"""

    FMT_INFO = 0
    """Info level index constant."""

    FMT_DEBUG = 1
    """Debug level index constant."""

    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARN': 'yellow',
        'ERROR': 'red',
        'CRIT': 'red,bg_white',
    }
    """Definition of color stream level setting."""

    def __init__(self,
                 is_save_file=None,
                 logdir=None,
                 backup_count=None,
                 filename=None,
                 is_debug_stream=None,
                 is_color_stream=None,
                 stream_level=None,
                 file_level=None,
                 date_fmt=None,
                 default=None):
        self.init_attr('is_save_file', is_save_file)
        self.init_attr('dirpath', logdir)
        self.init_attr('backup_count', backup_count)
        self.init_attr('filename', filename)
        self.init_attr('is_debug_stream', is_debug_stream)
        self.init_attr('is_color_stream', is_color_stream)
        self.init_attr('stream_level', stream_level)
        self.init_attr('file_level', file_level)
        self.init_attr('dete_fmt', date_fmt)
        self.init_attr('default', default)

        if self.is_debug_stream and self.stream_level == INFO:
            self.stream_level = DEBUG

        addLevelName(WARNING, 'WARN')
        addLevelName(CRITICAL, 'CRIT')

    def init_attr(self, key, value):
        """Initializing variables.

        If None, treat the value of the class variable as the in-
        stance argument otherwise.

        """

        if value is None:
            # class variable
            pass
        else:
            # instance variable
            setattr(self, key, value)

    @property
    def stream_fmt(self):
        """Return a stream fmt tailored to the situation."""
        return self._stream_fmt()

    def _stream_fmt(self, is_debug_stream=False):
        """Return a stream fmt tailored to the situation.

        Return fmt of color stream or debug stream according to set-
        ting situation.

        """

        is_debug_stream = is_debug_stream or self.is_debug_stream

        # Determine index of normal or debug.
        if is_debug_stream:
            index = self.FMT_DEBUG
        else:
            index = self.FMT_INFO

        # Determine normal or color fmts.
        if self.is_color_stream:
            fmts = self.stream_color_fmts
        else:
            fmts = self.stream_fmts

        return fmts[index]


class Delogger(DeloggerSetting):
    """A class that provides a decided logger.

    Args:
        name (str): Logger name
        parent (str): Log file save destination.
        *args: DeloggerSetting.
        **kwargs: DeloggerSetting.

    Attributes:
        _logger (logging.Logger): Logger.
        _is_new_logger (bool): Whether it is a first generation logger.

    """

    DEBUG = DEBUG
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR
    CRITICAL = CRITICAL

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
        """Return set logging.Logger."""

        # Set only loggers that have not been set yet.
        if self._is_new_logger and self.default:
            self.default_logger()
            self._is_new_logger = False

        return self._logger

    @classmethod
    def debuglog(cls, func):
        """When this decorator is set, the argument and return value are out-
        put to the log.
        """

        logger = cls(name='_debugger').logger

        def wrapper(*args, **kwargs):
            # Output function name and argument.
            msg = 'START {} args={} kwargs={}'.format(
                func.__qualname__,
                args,
                kwargs,
            )
            logger.debug(msg)

            # Output function name and return value.
            rtn = func(*args, **kwargs)
            msg = 'END {} return={}'.format(
                func.__qualname__,
                rtn,
            )
            logger.debug(msg)

            return rtn

        return wrapper

    def default_logger(self):
        """Set default handler."""
        self._logger.setLevel(DEBUG)

        if not self.is_debug_stream and self.stream_level <= INFO:
            # info is a normal stream, over warning it is a debug stream.
            fmt = self.stream_fmt
            self.add_stream_handler(
                self.stream_level,
                fmt=fmt,
                is_color_stream=self.is_color_stream,
                only_level=True)

            # Set warning or more stream
            fmt = self._stream_fmt(is_debug_stream=True)
            self.add_stream_handler(
                WARNING, fmt=fmt, is_color_stream=self.is_color_stream)

        else:
            # all debug stream.
            fmt = self.stream_fmt
            self.add_stream_handler(
                self.stream_level,
                fmt=fmt,
                is_color_stream=self.is_color_stream)
        # If there is a log save flag, the log file handler is set.

        if self.is_save_file:
            rrh = RunRotatingHandler(
                self.dirpath,
                backup_count=self.backup_count,
                fmt=self.filename)
            self.add_handler(rrh, DEBUG, fmt=self.file_fmt)

    def add_handler(self,
                    hdlr,
                    level,
                    fmt=None,
                    datefmt=None,
                    only_level=False,
                    formatter=None):
        """Helper function to add a handler.

        Args:
            hdlr: handler
            level (int): Handler level.
            fmt (str): Handler output format.
            datefmt (str): Handler output date format.
            only_level (bool): Whether to output only to specified han-
            dler level.
            formatter: Handler formatter.

        """

        hdlr.setLevel(level)

        # Set formatter.
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
                           is_color_stream=False,
                           hdlr=None,
                           **kwargs):
        """Helper function to add a stream handler.

        Args:
            level (int): Handler level.
            check_level (bool): Whether to check the default stream level.
            is_color_stream (bool): Whether to output in color stream.
            hdlr: Handler other than stream handler.
            **kwargs: Keyword argument of add_handler method

        """

        if check_level and self.stream_level <= level:
            return

        if is_color_stream:
            fmt = ColoredFormatter(
                kwargs.get('fmt', None),
                log_colors=self.log_colors,
                style='%',
            )
            kwargs.setdefault('formatter', fmt)

        hdlr = hdlr or StreamHandler()
        self.add_handler(hdlr, level, **kwargs)


class DeloggerQueue(Delogger):
    """Non-blocking Delogger using QueueHandler.

    Args:
        default (bool): Whether to use the default handler.
        *args: DeloggerSetting.
        *kwargs: DeloggerSetting.

    """

    _que = None
    """Queue used by QueueHandler."""

    _listener = None
    """A common QueueListener for all loggers."""

    def __init__(self, default=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = default

    def default_logger(self):
        """Default logger for Queue."""

        if not DeloggerQueue._listener:
            super().default_logger()

        self.queue_logger()

    def queue_logger(self):
        """Set up QueueHandler.

        Set QueueListener only for the first time.

        """

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
        """Stop the QueueListener at program exit."""
        if DeloggerQueue._listener:
            DeloggerQueue._listener.stop()
