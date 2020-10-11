import urllib.request
from unittest.mock import MagicMock


class UrlopenMock:
    def __init__(self):
        self._tmp_urlopen = urllib.request.urlopen
        self.load()

    def load(self):
        urllib.request.urlopen = MagicMock()

    def reset(self):
        urllib.request.urlopen = self._tmp_urlopen

    @property
    def call_count(self):
        return urllib.request.urlopen.call_count

    def assert_not_called(self):
        urllib.request.urlopen.assert_not_called()

    def __exit__(self):
        self.reset()
