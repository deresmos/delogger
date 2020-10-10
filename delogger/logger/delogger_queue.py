import atexit
from copy import copy
from logging import Logger
from queue import Queue
from typing import Optional

from delogger.logger.base import DeloggerBase


class DeloggerQueue(DeloggerBase):
    """Non-blocking Delogger using QueueHandler.

    Args:
        default (bool): Whether to use the default handler.
    """

    _que: Optional[Queue] = None
    """Queue used by QueueHandler."""

    _listener = None
    """A common QueueListener for all loggers."""

    def get_logger(self) -> Logger:
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
