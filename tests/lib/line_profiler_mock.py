from unittest.mock import MagicMock

import delogger.decorators.line_memory_profile
import delogger.decorators.line_profile


class LineProfilerMock(MagicMock):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_function = MagicMock()
        self.print_stats = MagicMock()
        self.runcall = MagicMock()
        self.__bool__ = MagicMock(return_value=True)

        delogger.decorators.line_profile.LineProfiler = self
        delogger.decorators.line_memory_profile.LineProfiler = self

    @property
    def return_value(self):
        return self
