from logging import DEBUG
from pathlib import Path
from typing import Optional

from delogger.base import DeloggerBase
from delogger.handlers import RunRotatingHandler
from delogger.modes.base import ModeBase


class LogFile:
    def __init__(self, filepath: str) -> None:
        _filepath = Path(filepath)

        self.filepath: Path = _filepath
        self.dirpath: Path = _filepath.parent
        self.filename: str = _filepath.name


class RunRotatingMode(ModeBase):
    def __init__(
        self,
        level: int = DEBUG,
        filepath: str = "log/%Y%m%d_%H%M%S.log",
        backup_count: int = 5,
        fmt: Optional[str] = None,
    ) -> None:
        self.level = level
        self.filepath = filepath
        self.backup_count = backup_count
        self.fmt = fmt

        self.logfile: Optional[LogFile] = None

    def load_handler(self, delogger: DeloggerBase):
        run_hdlr = RunRotatingHandler(
            filepath=self.filepath, backup_count=self.backup_count
        )

        fmt = self.fmt or delogger.file_fmt
        delogger.add_handler(run_hdlr, self.level, fmt=fmt)

        self.logfile = LogFile(run_hdlr.filepath)
