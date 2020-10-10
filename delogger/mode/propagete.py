from delogger.mode.base import ModeBase

__all__ = ["PropagateMode"]


class PropagateMode(ModeBase):
    def load(self, delogger) -> None:
        delogger.propagate(True)
