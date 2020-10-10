import logging

from delogger import DecoratorBase, ModeBase


class CustomDecorator(DecoratorBase):
    decorator_name = "custom"  # required

    # required
    def wrapper(self, f, *args, **kwargs):
        self.logger.debug("custom decorator")

        return f(*args, **kwargs)


class CustomMode(ModeBase):
    fmt = "%(asctime)s >> %(message)s"
    datefmt = "%Y:%m:%d"

    def load(self, delogger) -> None:
        delogger.add_stream_handler(logging.DEBUG, fmt=self.fmt, datefmt=self.datefmt)


if __name__ == "__main__":
    from delogger import Delogger

    delogger = Delogger("custom", modes=[CustomMode()], decorators=[CustomDecorator()])

    logger = delogger.get_logger()

    @logger.custom
    def test():
        logger.debug("test")

    test()
