import os
import re
from datetime import datetime as dt
from logging import FileHandler
from pathlib import Path
from typing import Dict, List, Optional


class _LOG_FILE(object):
    """Set the path of the log file.

    Args:
        dirname (str): Directory path.
        basename (str): Filename like date_string.

    Attributes:
        dirname (str): Directory path.
        basename (str): Filename like date_string.
        path (str): Log file path.

    """

    def __init__(self, dirname: str, basename: str) -> None:
        self.dirname = dirname
        self.basename = basename
        self.path: str = dt.today().strftime(str(Path(dirname) / basename))

    def __eq__(self, other):
        """Comparison for RunRotatingHandler.

        Returns:
            True if dirname is the same, False otherwise.

        """
        if not isinstance(other, _LOG_FILE):
            raise NotImplementedError
        eq = False
        eq = (other.dirname == self.dirname) and (other.basename == self.basename)

        return eq

    def __contains__(self, other):
        return other == self

    def __str__(self):
        return self.path


class RunRotatingHandler(FileHandler):
    """This handler leaves a log file for each execution.

    Args:
        dirname (str): Directory path.
        backup_count (int): Leave logs up to the designated generation.
        fmt (str): Filename like date_string.

    Attributes:
        filepath (str): File path determined only once at runtime.

    """

    LOG_FMT: str = "%Y%m%d_%H%M%S.log"
    """Default value of log format."""

    BACKUP_COUNT: int = 5
    """Default value of backup count."""

    _files: List[_LOG_FILE] = []
    """This list saving _LOG_FILE of output log file."""

    _LOG_FMT_RE: Dict[str, List[str]] = {
        r"\d{4}": ["%Y"],
        r"\d{2}": ["%m", "%d", "%H", "%M", "%S"],
    }

    def __init__(
        self,
        dirname: Optional[str] = None,
        filepath: Optional[str] = None,
        backup_count: Optional[int] = None,
        fmt: Optional[str] = None,
        **kwargs
    ):
        fmt = fmt or self.LOG_FMT
        backup_count = backup_count or self.BACKUP_COUNT

        if filepath:
            dirname = str(Path(filepath).parent)
            fmt = Path(filepath).name
        self.filepath = self._load_file_path(str(dirname), fmt, backup_count)

        super().__init__(self.filepath, **kwargs)

    def _open(self):
        """It is executed at log output.

        If there is no directory, it will be created automatically.

        """

        # If there is no save destination directory, the directory is created.
        path_parent = Path(self.filepath).parent
        if not path_parent.is_dir():
            os.makedirs(str(path_parent))

        return super()._open()

    def _load_file_path(self, dirname: str, fmt: str, backup_count: int) -> str:
        """Get the file path of the log output destination.

        For each directory, determine the log file path only once at runtime.

        Args:
            dirname (str): Directory path.
            fmt (str): Filename like date_string.
            backup_count (int): Leave logs up to the designated generation.

        """

        # Set the logfile name.
        path = _LOG_FILE(dirname, fmt)
        filepath = Path(str(path))

        # If already same dirname, return the filepath.
        for fpath in RunRotatingHandler._files:
            if fpath == path:
                return str(fpath)

        # Get a file list that matches the format of fmt.
        filenames = self._get_match_files(filepath.parent, fmt)

        # Delete the old file and set a new file path
        if (backup_count > 0) and (len(filenames) >= backup_count):
            os.remove(filenames[0])
        RunRotatingHandler._files.append(path)

        return str(path)

    def _get_match_files(self, dirpath, fmt) -> List[Path]:
        fmt_ = fmt
        for patter, date_strs in self._LOG_FMT_RE.items():
            for date_str in date_strs:
                fmt_ = fmt_.replace(date_str, patter)

        repa = re.compile(fmt_)
        files = [x for x in sorted(Path(dirpath).glob("*")) if repa.search(str(x))]

        return files
