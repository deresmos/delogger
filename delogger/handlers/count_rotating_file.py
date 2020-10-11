from logging import FileHandler
import os
from pathlib import Path
import re
from typing import Dict
from typing import List

from delogger.util.log_file import LogFile

__all__ = ["CountRotatingFileHandler"]


class CountRotatingFileHandler(FileHandler):
    """This handler to keep the saved log count.

    Args:
        filepath (str): log filepath.
        backup_count (int): Leave logs up to the designated generation.

    Attributes:
        filepath (str): File path determined only once at runtime.

    """

    _files: List[LogFile] = []
    """This list saving LogFile of output log file."""

    _LOG_FMT_RE: Dict[str, List[str]] = {
        r"\d{4}": ["%Y"],
        r"\d{2}": ["%m", "%d", "%H", "%M", "%S"],
        r"\d{6}": ["%f"],
    }

    def __init__(self, filepath: str, backup_count: int = 5) -> None:
        dirpath = str(Path(filepath).parent)
        fmt = Path(filepath).name

        self.logfile = self._load_file_path(dirpath, fmt, backup_count)
        self.filepath = str(self.logfile.filepath)

        super().__init__(self.filepath)

    def _open(self):
        """It is executed at log output.

        If there is no directory, it will be created automatically.

        """

        # If there is no save destination directory, the directory is created.
        self.logfile.mkdir()

        return super()._open()

    def _load_file_path(self, dirpath: str, fmt: str, backup_count: int) -> LogFile:
        """Get the file path of the log output destination.

        For each directory, determine the log file path only once at runtime.

        Args:
            dirpath (str): Directory path.
            fmt (str): Filename like date_string.
            backup_count (int): Leave logs up to the designated generation.

        """

        logfile = LogFile(str(Path(dirpath) / fmt))

        # If already same logfile, return the filepath.
        for fpath in CountRotatingFileHandler._files:
            if fpath == logfile:
                return fpath
        CountRotatingFileHandler._files.append(logfile)

        if backup_count <= 0:
            return logfile

        file_list = self._get_match_files(logfile.filepath.parent, fmt)

        # Delete the old file and set a new filepath
        if len(file_list) >= backup_count:
            os.remove(file_list[0])
        return logfile

    def _get_match_files(self, dirpath, fmt) -> List[Path]:
        _fmt = fmt
        for patter, date_strs in self._LOG_FMT_RE.items():
            for date_str in date_strs:
                _fmt = _fmt.replace(date_str, patter)

        # TODO: check file stat?? datefmt only ok??
        pattern = re.compile(_fmt)
        files = [x for x in sorted(Path(dirpath).glob("*")) if pattern.search(str(x))]

        return files
