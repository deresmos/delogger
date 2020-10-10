import os
import re
from datetime import datetime as dt
from logging import FileHandler
from pathlib import Path
from typing import Dict, List

__all__ = ["CountRotatingFileHandler"]


class LogFile(object):
    """Set the path of the log file.

    Args:
        filepath (str): Log file path.

    Attributes:
        filepath (Path): Log file path.
        filepath_raw (str): Log file path raw.

    """

    def __init__(self, filepath: str) -> None:
        self.filepath: Path = Path(dt.today().strftime(filepath))
        self.filepath_raw: Path = Path(filepath)

    def __eq__(self, other):
        """Comparison for CountRotatingFileHandler.

        Returns:
            True if dirpath is the same, False otherwise.

        """
        if not isinstance(other, LogFile):
            raise NotImplementedError

        return other.filepath_raw.absolute() == self.filepath_raw.absolute()

    def __contains__(self, other):
        return other == self

    def __str__(self):
        return str(self.filepath)


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

    def __init__(self, filepath, backup_count=5) -> None:
        dirpath = str(Path(filepath).parent)
        fmt = Path(filepath).name

        self.filepath: str = self._load_file_path(dirpath, fmt, backup_count)

        super().__init__(self.filepath)

    def _open(self):
        """It is executed at log output.

        If there is no directory, it will be created automatically.

        """

        # If there is no save destination directory, the directory is created.
        path_parent = Path(self.filepath).parent
        if not path_parent.is_dir():
            os.makedirs(str(path_parent))

        return super()._open()

    def _load_file_path(self, dirpath: str, fmt: str, backup_count: int) -> str:
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
                return str(fpath)
        CountRotatingFileHandler._files.append(logfile)

        if backup_count <= 0:
            return str(logfile)

        file_list = self._get_match_files(logfile.filepath.parent, fmt)

        # Delete the old file and set a new filepath
        if len(file_list) >= backup_count:
            os.remove(file_list[0])

        return str(logfile)

    def _get_match_files(self, dirpath, fmt) -> List[Path]:
        _fmt = fmt
        for patter, date_strs in self._LOG_FMT_RE.items():
            for date_str in date_strs:
                _fmt = _fmt.replace(date_str, patter)

        # TODO: check file stat??
        pattern = re.compile(_fmt)
        files = [x for x in sorted(Path(dirpath).glob("*")) if pattern.search(str(x))]

        return files
