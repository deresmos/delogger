import atexit
from copy import copy
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Formatter,
    StreamHandler,
    getLogger,
)
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

from colorlog import ColoredFormatter
from delogger import OnlyFilter, RunRotatingHandler
from delogger.setting import DeloggerSetting

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from line_profiler import LineProfiler
except ImportError:
    pass

try:
    from memory_profiler import profile
except ImportError:
    pass


class LineEmpty(Exception):
    pass


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

    L_M_HEADER_INDEX = 6
    L_M_SEPARATOR_INDEX = 7
    L_M_TEMPLATE = "{0:>6} {1:>9} {2:>12} {3:>8} {4:>8} " "{5:>12} {6:>12}   {7:<}"
    L_M_HEADER = [
        "Line #",
        "Hits",
        "Time",
        "Per Hit",
        "% Time",
        "Mem usage",
        "Increment",
        "Line Contents",
    ]

    def __init__(self, name=None, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        name_ = parent or self
        name_ = name or type(name_).__name__
        logger = getLogger(name_)
        logger.setLevel(Delogger.DEBUG)
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
            self._logger.propagate = False
            self._is_new_logger = False

        return self._logger

    @classmethod
    def debuglog(cls, func):
        """When this decorator is set, the argument and return value are out-
        put to the log.
        """

        logger = cls(name="_debugger").logger

        def wrapper(*args, **kwargs):
            # Output function name and argument.
            msg = "START {} args={} kwargs={}".format(func.__qualname__, args, kwargs)
            logger.debug(msg)

            # Output function name and return value.
            rtn = func(*args, **kwargs)
            msg = "END {} return={}".format(func.__qualname__, rtn)
            logger.debug(msg)

            return rtn

        return wrapper

    @classmethod
    def line_profiler(cls, func):
        """line_profiler are output to the log.
        """

        logger = cls(name="_debugger_l").logger

        def wrapper(*args, **kwargs):
            # output line_profiler
            prof = LineProfiler()
            prof.add_function(func)

            rtn = prof.runcall(func, *args, **kwargs)
            with StringIO() as f:
                prof.print_stats(stream=f)
                msg = "line_profiler result\n{}".format(f.getvalue())
            logger.debug(msg)

            return rtn

        return wrapper

    @classmethod
    def memory_profiler(cls, func):
        """memory_profiler are output to the log.
        """

        logger = cls(name="_debugger_m").logger

        def wrapper(*args, **kwargs):
            # output memory_profiler
            with StringIO() as f:
                rtn = profile(func, stream=f, precision=2)(*args, **kwargs)
                msg = "memory_profiler result\n{}".format(f.getvalue())
            logger.debug(msg)

            return rtn

        return wrapper

    @classmethod
    def line_memory_profiler(cls, func):
        """line_profiler and memory_profiler mix are output to the log.
        """

        logger = cls(name="_debugger_l_m").logger

        def wrapper(*args, **kwargs):
            # memory_profiler
            with StringIO() as f:
                rtn = profile(func, stream=f, precision=2)(*args, **kwargs)
                memory_value = cls._memory_profiler_parse(f.getvalue())

            # line_profiler
            prof = LineProfiler()
            prof.add_function(func)

            rtn = prof.runcall(func, *args, **kwargs)
            with StringIO() as f:
                prof.print_stats(stream=f)
                mix, line_tmp = cls._line_profiler_parse(f.getvalue())

            # memory line mix output
            template = cls.L_M_TEMPLATE
            for l, m in zip(line_tmp, memory_value):
                l_m_mix = l[:5] + m
                mix.append(template.format(*l_m_mix))
            mix[cls.L_M_HEADER_INDEX] = template.format(*cls.L_M_HEADER)
            mix[cls.L_M_SEPARATOR_INDEX] += "=" * 27
            logger.debug("line, memory profiler result\n" + "\n".join(mix))

            return rtn

        return wrapper

    @staticmethod
    def _memory_profiler_parse(result):
        for line in result.split("\n"):
            try:
                elem = line.split()
                if not elem:
                    continue

                lineno = elem[0].isnumeric()
                if not lineno:
                    continue

                contents = line[35:]
                if len(elem) < 2:
                    raise LineEmpty()
                float(elem[1])

                mem = elem[1:3]
                inc_mem = elem[3:5]
                yield [" ".join(mem), " ".join(inc_mem), contents]

            except ValueError:
                yield ["", "", contents]
                continue
            except LineEmpty:
                yield ["", "", ""]
                continue

    @staticmethod
    def _line_profiler_parse(result):
        mix = []
        line_tmp = []
        for line in result.split("\n"):
            try:
                elem = line.split()
                if not elem:
                    mix.append(line)
                    continue

                is_lineno = elem[0].isnumeric()
                if not is_lineno:
                    mix.append(line)
                    continue

                if len(elem) < 2:
                    raise LineEmpty()
                float(elem[1])
                line_tmp.append(elem[:5])

            except ValueError:
                line_tmp.append([elem[0], "", "", "", ""])
                continue
            except LineEmpty:
                line_tmp.append([elem[0], "", "", "", ""])
                continue

        for _ in range(5):
            if not mix[-1]:
                del mix[-1]
            else:
                break

        return mix, line_tmp

    def default_logger(self):
        """Set default handler."""

        if not self.is_debug_stream and self.stream_level <= INFO:
            # info is a normal stream, over warning it is a debug stream.
            fmt = self.stream_fmt
            self.add_stream_handler(
                self.stream_level,
                fmt=fmt,
                is_color_stream=self.is_color_stream,
                only_level=True,
            )

            # Set warning or more stream
            fmt = self._stream_fmt(is_debug_stream=True)
            self.add_stream_handler(
                WARNING, fmt=fmt, is_color_stream=self.is_color_stream
            )

        else:

            stream_level = self.stream_level
            if self.is_debug_stream and self.stream_level == INFO:
                stream_level = DEBUG

            # all debug stream.
            fmt = self.stream_fmt
            self.add_stream_handler(
                stream_level, fmt=fmt, is_color_stream=self.is_color_stream
            )
        # If there is a log save flag, the log file handler is set.

        if self.is_save_file:
            rrh = RunRotatingHandler(
                self.dirpath,
                backup_count=self.backup_count,
                filepath=self.filepath,
                fmt=self.filename,
            )
            self.add_handler(rrh, DEBUG, fmt=self.file_fmt)

    def add_handler(
        self, hdlr, level, fmt=None, datefmt=None, only_level=False, formatter=None
    ):
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

    def add_stream_handler(
        self, level, *, check_level=False, is_color_stream=False, hdlr=None, **kwargs
    ):
        """Helper function to add a stream handler.

        Args:
            level (int): Handler level.
            check_level (bool): Whether to check the default stream level.
            is_color_stream (bool): Whether to output in color stream.
            hdlr: Handler other than stream handler.
            **kwargs: Keyword argument of add_handler method

        """

        # disable stream output
        if not self.is_stream:
            return

        if check_level and self.stream_level <= level:
            return

        if is_color_stream:
            fmt = ColoredFormatter(
                kwargs.get("fmt", None), log_colors=self.log_colors, style="%"
            )
            kwargs.setdefault("formatter", fmt)

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
            listener = QueueListener(que, *handlers, respect_handler_level=True)
            self._logger.addHandler(queue_handler)
            listener.start()

            DeloggerQueue._que = que
            DeloggerQueue._listener = listener

            atexit.register(self.listener_stop)

    def listener_stop(self):
        """Stop the QueueListener at program exit."""
        if DeloggerQueue._listener:
            DeloggerQueue._listener.stop()
