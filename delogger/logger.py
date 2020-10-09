import atexit
from copy import copy
from logging import DEBUG, INFO, WARNING, Logger
from queue import Queue
from typing import List, Optional

from delogger.base import DeloggerBase
from delogger.decorators.base import DecoratorBase
from delogger.modes.base import ModeBase


class Delogger(DeloggerBase):
    def __init__(
        self,
        name: Optional[str] = None,
        modes: Optional[List[ModeBase]] = None,
        decorators: Optional[List[DecoratorBase]] = None,
        **kwargs
    ) -> None:
        super().__init__(name=name, **kwargs)

        if modes:
            self.load_modes(*modes)

        if decorators:
            self.load_decorators(*decorators)

    def get_logger(self) -> Logger:
        """Return set logging.Logger."""

        if self.is_already_setup():
            return self._logger

        # Set handler
        self._is_new_logger = False

        return self._logger

    def load_modes(self, *modes) -> None:
        if self.is_already_setup():
            return

        for mode in modes:
            mode.load_to_delogger(delogger=self)

    def load_decorators(self, *decorators) -> None:
        if self.is_already_setup():
            return

        for decorator in decorators:
            decorator.load_to_delogger(delogger=self)


class DeloggerQueue(Delogger):
    """Non-blocking Delogger using QueueHandler.

    Args:
        default (bool): Whether to use the default handler.
    """

    _que: Optional[Queue] = None
    """Queue used by QueueHandler."""

    _listener = None
    """A common QueueListener for all loggers."""

    def get_logger(self) -> Logger:
        """Return set logging.Logger."""

        if not DeloggerQueue._listener:
            self.queue_logger()

        return super().get_logger()

    def queue_logger(self) -> None:
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

            que: Queue = Queue(-1)
            queue_handler = QueueHandler(que)
            listener = QueueListener(que, *handlers, respect_handler_level=True)
            self._logger.addHandler(queue_handler)
            listener.start()

            DeloggerQueue._que = que
            DeloggerQueue._listener = listener

            atexit.register(self.listener_stop)

    def listener_stop(self) -> None:
        """Stop the QueueListener at program exit."""
        if DeloggerQueue._listener:
            DeloggerQueue._listener.stop()
