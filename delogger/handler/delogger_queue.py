from logging.handlers import QueueHandler
from logging.handlers import QueueListener


class DeloggerQueueHandler(QueueHandler):
    def __init__(self, listener: QueueListener, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.listener = listener
        self.start()

    def start(self) -> None:
        self.listener.start()

    def join(self) -> None:
        self.listener.queue.join()  # type: ignore

    def close(self, *args, **kwargs):
        if self.listener._thread:  # pragma: no cover
            self.listener.stop()  # pragma: no cover

        super().close(*args, **kwargs)  # pragma: no cover
