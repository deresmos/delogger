from delogger.modes.base import ModeBase

__all__ = ["PropagateMode"]


class PropagateMode(ModeBase):
    def load_to_delogger(self, delogger) -> None:
        delogger._logger.propagate = True
