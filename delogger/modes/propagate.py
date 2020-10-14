from delogger.modes.base import ModeBase

__all__ = ["NotPropagateMode"]


class NotPropagateMode(ModeBase):
    def load(self, delogger) -> None:
        delogger.propagate = False
