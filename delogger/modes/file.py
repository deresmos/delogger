from logging import DEBUG
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

from delogger.handlers.run_rotating import RunRotatingHandler
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


class FileMode(ModeBase):
    file_fmt = (
        "%(asctime)s.%(msecs).03d %(levelname)s %(filename)s:%(lineno)d %(message)s"
    )
    """Default value of file logger fmt."""

    date_fmt = "%Y-%m-%d %H:%M:%S"
    """Default value of datetime format."""

    def __init__(self, fmt: Optional[str] = None, date_fmt: Optional[str] = None):
        self.fmt = fmt or self.file_fmt
        self.date_fmt = date_fmt or self.date_fmt


class RunRotatingFileMode(FileMode):
    def __init__(
        self,
        filepath: str = "log/%Y%m%d_%H%M%S.log",
        backup_count: int = 5,
        level: int = DEBUG,
        fmt: Optional[str] = None,
        date_fmt: Optional[str] = None,
    ) -> None:
        super().__init__(fmt=fmt, date_fmt=date_fmt)

        self.level = level
        self.filepath = filepath
        self.backup_count = backup_count

        self.logfile: Optional[LogFile] = None

    def load_to_delogger(self, delogger):
        run_hdlr = RunRotatingHandler(
            filepath=self.filepath, backup_count=self.backup_count
        )

        delogger.add_handler(run_hdlr, self.level, fmt=self.fmt, datefmt=self.date_fmt)

        self.logfile = LogFile(run_hdlr.filepath)


class TimedRotatingFileMode(FileMode):
    def __init__(
        self,
        filepath: str = "log/delogger.log",
        when: str = "midnight",
        backup_count: int = 0,
        level: int = DEBUG,
        fmt: Optional[str] = None,
        date_fmt: Optional[str] = None,
    ) -> None:
        super().__init__(fmt=fmt, date_fmt=date_fmt)

        self.level = level
        self.filepath = filepath
        self.when = when
        self.backup_count = backup_count

        self.logfile = LogFile(filepath)

    def load_to_delogger(self, delogger):
        self.logfile.mkdir()
        timed_hdlr = TimedRotatingFileHandler(
            filename=str(self.logfile.filepath),
            when=self.when,
            backupCount=self.backup_count,
        )

        delogger.add_handler(
            timed_hdlr, self.level, fmt=self.fmt, datefmt=self.date_fmt
        )
