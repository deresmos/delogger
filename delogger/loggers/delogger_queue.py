from logging import Logger
from logging import NOTSET
from logging.handlers import QueueListener
from queue import Queue
from typing import Optional

from delogger.handlers.delogger_queue import DeloggerQueueHandler
from delogger.loggers.base import DeloggerBase


class DeloggerQueue(DeloggerBase):
    """Non-blocking Delogger using DeloggerQueueHandler.

    Args:
        default (bool): Whether to use the default handler.
    """

    _queue_hdlr: Optional[DeloggerQueueHandler] = None
    """A common QueueListener for all loggers."""

    def get_logger(self) -> Logger:
        if not self.is_already_setup():
            self.queue_logger()
        else:
            self._queue_hdlr: Optional[DeloggerQueueHandler] = self._find_queue_hdlr(
                self._logger.handlers
            )

        return super().get_logger()

    def queue_logger(self) -> None:
        """Set up DeloggerQueueHandler.

        Set QueueListener only for the first time.

        """
        # init que and listener
        handlers = self._logger.handlers[:]
        for hdlr in handlers:
            self._logger.removeHandler(hdlr)

        que: Queue = Queue(-1)
        listener = QueueListener(que, *handlers, respect_handler_level=True)
        queue_handler = DeloggerQueueHandler(listener, que)
        self.add_handler(queue_handler, NOTSET)

        self._queue_hdlr = queue_handler

    def join(self) -> bool:
        if not self._queue_hdlr:
            return False

        self._queue_hdlr.join()
        return True

    def _find_queue_hdlr(self, handlers) -> Optional[DeloggerQueueHandler]:
        for handler in handlers:
            if isinstance(handler, DeloggerQueueHandler):
                return handler

        return None
