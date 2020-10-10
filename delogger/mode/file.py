from logging import DEBUG
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

from delogger.handler.count_rotating_file import CountRotatingFileHandler
from delogger.mode.base import ModeBase

__all__ = ["CountRotatingFileMode", "TimedRotatingFileMode"]


class LogFile:
    def __init__(self, filepath: str) -> None:
        _filepath = Path(filepath)

        self.filepath: Path = _filepath
        self.dirpath: Path = _filepath.parent
        self.filename: str = _filepath.name

        self.mkdir()

    def mkdir(self) -> None:
        if self.dirpath.is_dir():
            return

        self.dirpath.mkdir(parents=True, exist_ok=True)


class FileModeBase(ModeBase):
    fmt = "%(asctime)s.%(msecs).03d %(levelname)s %(filename)s:%(lineno)d %(funcName)s %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"


class CountRotatingFileMode(FileModeBase):
    def __init__(
        self,
        filepath: str = "log/%Y%m%d_%H%M%S.log",
        backup_count: int = 5,
        level: int = DEBUG,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.level = level
        self.filepath = filepath
        self.backup_count = backup_count

        self.logfile: Optional[LogFile] = None

    def load(self, delogger) -> None:
        run_hdlr = CountRotatingFileHandler(
            filepath=self.filepath, backup_count=self.backup_count
        )

        delogger.add_handler(run_hdlr, self.level, fmt=self.fmt, datefmt=self.datefmt)

        self.logfile = LogFile(run_hdlr.filepath)


class TimedRotatingFileMode(FileModeBase):
    def __init__(
        self,
        filepath: str = "log/delogger.log",
        when: str = "midnight",
        backup_count: int = 0,
        level: int = DEBUG,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.level = level
        self.filepath = filepath
        self.when = when
        self.backup_count = backup_count

        self.logfile = LogFile(filepath)

    def load(self, delogger) -> None:
        timed_hdlr = TimedRotatingFileHandler(
            filename=str(self.logfile.filepath),
            when=self.when,
            backupCount=self.backup_count,
        )

        delogger.add_handler(timed_hdlr, self.level, fmt=self.fmt, datefmt=self.datefmt)
