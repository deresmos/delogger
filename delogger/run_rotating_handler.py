import os
from datetime import datetime as dt
from logging import FileHandler
from pathlib import Path


class _FILE_PATH(object):
    def __init__(self, dirname, basename):
        self.dirname = dirname
        self.basename = basename
        self.path = dt.today().strftime(str(Path(dirname) / basename))

    def __eq__(self, other):
        if not isinstance(other, _FILE_PATH):
            raise NotImplemented
        eq = False
        eq = other.dirname == self.dirname

        return eq

    def __contains__(self, other):
        return other == self

    def __str__(self):
        return self.path


class RunRotatingHandler(FileHandler):
    LOG_FMT = '%Y%m%d_%H%M%S.log'
    BACKUP_COUNT = 5

    _files = []

    def __init__(self, dirname, backup_count=None, fmt=None, **kwargs):
        fmt = fmt or self.LOG_FMT
        backup_count = backup_count or self.BACKUP_COUNT

        self.filepath = self._load_file_path(dirname, fmt, backup_count)

        super().__init__(self.filepath, **kwargs)

    def _open(self):
        path_parent = Path(self.filepath).parent
        if not path_parent.is_dir():
            os.makedirs(path_parent)

        super()._open()

    def _load_file_path(self, dirname, fmt, backup_count):
        # Set the logfile name
        path = _FILE_PATH(dirname, fmt)
        filepath = Path(str(path))

        # If already same dirname, return the filepath
        for fpath in RunRotatingHandler._files:
            if fpath == path:
                return str(fpath)

        # Get file list matching format
        filenames = sorted(filepath.parent.glob('*'))

        # Delete the old file and set a new file path
        if len(filenames) >= backup_count:
            os.remove(filenames[0])

        RunRotatingHandler._files.append(path)
        return str(path)
