from logging import DEBUG
from logging.handlers import TimedRotatingFileHandler
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

    def mkdir(self) -> None:
        if self.dirpath.is_dir():
            return

        self.dirpath.mkdir(parents=True, exist_ok=True)


class RunRotatingFileMode(ModeBase):
    def __init__(
        self,
        filepath: str = "log/%Y%m%d_%H%M%S.log",
        backup_count: int = 5,
        level: int = DEBUG,
        fmt: Optional[str] = None,
    ) -> None:
        self.level = level
        self.filepath = filepath
        self.backup_count = backup_count
        self.fmt = fmt

        self.logfile: Optional[LogFile] = None

    def load_mode(self, delogger: DeloggerBase):
        run_hdlr = RunRotatingHandler(
            filepath=self.filepath, backup_count=self.backup_count
        )

        fmt = self.fmt or delogger.file_fmt
        delogger.add_handler(run_hdlr, self.level, fmt=fmt)

        self.logfile = LogFile(run_hdlr.filepath)


class TimedRotatingFileMode(ModeBase):
    def __init__(
        self,
        filepath: str = "log/delogger.log",
        when: str = "midnight",
        backup_count: int = 0,
        level: int = DEBUG,
        fmt: Optional[str] = None,
    ) -> None:
        self.level = level
        self.filepath = filepath
        self.when = when
        self.backup_count = backup_count
        self.fmt = fmt

        self.logfile = LogFile(filepath)

    def load_mode(self, delogger: DeloggerBase):
        self.logfile.mkdir()
        timed_hdlr = TimedRotatingFileHandler(
            filename=str(self.logfile.filepath),
            when=self.when,
            backupCount=self.backup_count,
        )

        fmt = self.fmt or delogger.file_fmt
        delogger.add_handler(timed_hdlr, self.level, fmt=fmt)
