from logging import DEBUG, Formatter, StreamHandler, getLogger

from delogger import OnlyFilter
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
        logger.propagate = False
        self._logger = logger

        if len(self._logger.handlers) > 0:
            # Already set logger
            self._is_new_logger = False
        else:
            # Not set logger
            self._is_new_logger = True

    def is_already_setup(self):
        return not self._is_new_logger

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
        self,
        level,
        *,
        check_level=False,
        is_color_stream=False,
        hdlr=None,
        datefmt=None,
        log_colors=None,
        **kwargs
    ):
        """Helper function to add a stream handler.

        Args:
            level (int): Handler level.
            check_level (bool): Whether to check the default stream level.
            is_color_stream (bool): [Deprecated] Whether to output in color stream.
            hdlr: Handler other than stream handler.
            **kwargs: Keyword argument of add_handler method

        """

        # disable stream output
        if not self.is_stream:
            return

        if check_level and self.stream_level <= level:
            return

        # deprecated is_color_stream
        if is_color_stream:
            from colorlog import ColoredFormatter

            datefmt = datefmt or self.date_fmt
            # deprecated self.log_colors
            log_colors = log_colors or self.log_colors
            fmt = ColoredFormatter(
                kwargs.get("fmt", None),
                log_colors=log_colors,
                style="%",
                datefmt=datefmt,
            )
            kwargs.setdefault("formatter", fmt)

        hdlr = hdlr or StreamHandler()
        self.add_handler(hdlr, level, datefmt=datefmt, **kwargs)

    def add_color_stream_handler(
        self, level, log_colors, *, check_level=False, hdlr=None, datefmt=None, **kwargs
    ):
        """Helper function to add a color stream handler.

        Args:
            level (int): Handler level.
            check_level (bool): Whether to check the default stream level.
            hdlr: Handler other than stream handler.
            **kwargs: Keyword argument of add_handler method

        """

        if check_level and self.stream_level <= level:
            return

        from colorlog import ColoredFormatter

        datefmt = datefmt or self.date_fmt
        # deprecated self.log_colors
        log_colors = log_colors or self.log_colors
        fmt = ColoredFormatter(
            kwargs.get("fmt", None), log_colors=log_colors, style="%", datefmt=datefmt
        )

        hdlr = hdlr or StreamHandler()
        self.add_handler(hdlr, level, datefmt=datefmt, formatter=fmt, **kwargs)
