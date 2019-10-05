from logging import DEBUG, INFO, WARNING, Formatter, StreamHandler, getLogger

from colorlog import ColoredFormatter
from delogger import OnlyFilter, RunRotatingHandler
from delogger.setting import DeloggerSetting


class DeloggerBase(DeloggerSetting):
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

    def __init__(self, name=None, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        name_ = parent or self
        name_ = name or type(name_).__name__
        logger = getLogger(name_)
        logger.setLevel(DEBUG)
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
