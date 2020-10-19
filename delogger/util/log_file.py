from datetime import datetime as dt
from pathlib import Path

__all__ = ["LogFile"]


class LogFile:
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

    def mkdir(self) -> None:
        dirpath = self.filepath.parent
        if dirpath.is_dir():
            return

        dirpath.mkdir(parents=True, exist_ok=True)

    def __eq__(self, other):
        """Comparison for CountRotatingFileHandler.

        Returns:
            True if dirpath is the same, False otherwise.

        """
        if not isinstance(other, LogFile):
            raise NotImplementedError

        return other.filepath.absolute() == self.filepath.absolute()

    def __contains__(self, other):
        return other == self

    def __str__(self):
        return str(self.filepath)
