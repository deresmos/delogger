from typing import Optional

from delogger.decorators.base import DecoratorBase


class DebugLog(DecoratorBase):
    decorator_name = "debuglog"

    START_MESSAGE: str = "START {func_name} args={args} kwargs={kwargs}"
    END_MESSAGE: str = "END {func_name} return={return}"

    def __init__(
        self, start_message: Optional[str] = None, end_message: Optional[str] = None
    ) -> None:
        super().__init__()

        self.start_message: str = start_message or self.START_MESSAGE
        self.end_message: str = end_message or self.END_MESSAGE

    def wrapper(self, f, *args, **kwargs):
        # Output function name and argument.
        msg = self.start_message.format(
            **{"func_name": f.__qualname__, "args": args, "kwargs": kwargs}
        )
        self.logger.debug(msg)

        # Output function name and return value.
        rtn = f(*args, **kwargs)
        msg = self.end_message.format(**{"func_name": f.__qualname__, "return": rtn})
        self.logger.debug(msg)

        return rtn
