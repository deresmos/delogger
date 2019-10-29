import atexit
from copy import copy
from logging import DEBUG, INFO, WARNING
from queue import Queue
from typing import Optional

from delogger.base import DeloggerBase
from delogger.handlers.run_rotating import RunRotatingHandler
from delogger.modes.base import ModeBase
from delogger.modes.stream import ColorStreamInfoMode


class Delogger(DeloggerBase):
    DEFAULT_MODES = [ColorStreamInfoMode()]

    def __init__(
        self, name: str = None, *, modes: Optional[ModeBase] = None, **kwargs
    ) -> None:
        super().__init__(name=name, **kwargs)

        self.modes = modes or self.DEFAULT_MODES

    @property
    def logger(self):
        """Return set logging.Logger."""

        # Set only loggers that have not been set yet.
        if self._is_new_logger and self.default:
            self.default_logger()
            self._is_new_logger = False

        return self._logger

    def get_logger(self):
        """Return set logging.Logger."""

        if not self._is_new_logger:
            return self._logger

        # Set handler
        self.load_modes(self.modes)
        self._is_new_logger = False

        return self._logger

    def load_modes(self, modes):
        for mode in modes:
            mode.load_mode(delogger=self)

    def load_decorators(self, *decorators):
        for decorator in decorators:
            decorator.load_to_delogger(delogger=self)

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
        from logging.handlers import QueueHandler, QueueListener

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
