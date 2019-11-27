from logging import CRITICAL, DEBUG, INFO, WARNING, addLevelName


class DeloggerSettingBase:
    def init_attr(self, key, value):
        """Initializing variables.

        If None, treat the value of the class variable as the in-
        stance argument otherwise.

        """

        if value is None:
            # class variable
            pass
        else:
            # instance variable
            setattr(self, key, value)


class DeloggerFileSetting(DeloggerSettingBase):
    is_save_file = False
    """[Deprecated] Default value of save file flag."""

    file_level = DEBUG
    """[Deprecated] Default value of file logger level."""

    dirpath = "log"
    """[Deprecated] Default value of log output destination directory."""

    backup_count = 5
    """[Deprecated] Default value of RunRotatingHandler backup count."""

    filename = None
    """[Deprecated] Default value of RunRotatingHandler filename (fmt)."""

    filepath = None
    """[Deprecated] Default value of RunRotatingHandler filepath (filepath)."""

    file_fmt = (
        "%(asctime)s.%(msecs).03d %(levelname)s %(filename)s:%(lineno)d %(message)s"
    )
    """Default value of file logger fmt."""

    def __init__(
        self,
        is_save_file=None,
        file_level=None,
        dirpath=None,
        backup_count=None,
        filename=None,
        filepath=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.init_attr("is_save_file", is_save_file)
        self.init_attr("file_level", file_level)
        self.init_attr("dirpath", dirpath)
        self.init_attr("backup_count", backup_count)
        self.init_attr("filename", filename)
        self.init_attr("filepath", filepath)


class DeloggerStreamSetting(DeloggerSettingBase):
    is_stream = True
    """[Deprecated] Default value of stream output flag."""

    is_debug_stream = False
    """[Deprecated] Default value of debug stream flag."""

    is_color_stream = True
    """[Deprecated] Default value of color stream flag."""

    stream_level = INFO
    """[Deprecated] Default value of stream logger level."""

    stream_fmts = [
        "%(message)s",
        (
            '%(levelname)-5s [%(name)s File "%(filename)s", '
            "line %(lineno)d, in %(funcName)s] %(message)s"
        ),
    ]
    """Default value of stream logger fmt.(0: normal, 1: debug)"""

    stream_color_fmts = [
        "%(message)s",
        (
            "%(log_color)s%(levelname)-5s%(reset)s [%(name)s "
            'File "%(filename)s", line %(lineno)d, in %(funcName)s] %(message)s'
        ),
    ]
    """Default value of color stream logger fmt.(0: normal, 1: debug)"""

    FMT_INFO = 0
    """Info level index constant."""

    FMT_DEBUG = 1
    """Debug level index constant."""

    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARN": "yellow",
        "ERROR": "red",
        "CRIT": "red,bg_white",
    }
    """Definition of color stream level setting."""

    def __init__(
        self,
        is_stream=None,
        is_debug_stream=None,
        is_color_stream=None,
        stream_level=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.init_attr("is_stream", is_stream)
        self.init_attr("is_debug_stream", is_debug_stream)
        self.init_attr("is_color_stream", is_color_stream)
        self.init_attr("stream_level", stream_level)

    @property
    def stream_fmt(self):
        """[Deprecated] Return a stream fmt tailored to the situation."""
        return self._stream_fmt()

    def _stream_fmt(self, is_debug_stream=False):
        """[Deprecated] Return a stream fmt tailored to the situation.

        Return fmt of color stream or debug stream according to set-
        ting situation.

        """

        is_debug_stream = is_debug_stream or self.is_debug_stream

        # Determine index of normal or debug.
        if is_debug_stream:
            index = self.FMT_DEBUG
        else:
            index = self.FMT_INFO

        # Determine normal or color fmts.
        if self.is_color_stream:
            fmts = self.stream_color_fmts
        else:
            fmts = self.stream_fmts

        return fmts[index]


class DeloggerSetting(DeloggerFileSetting, DeloggerStreamSetting):
    date_fmt = "%Y-%m-%d %H:%M:%S"
    """Default value of datetime format."""

    default = True
    """[Deprecated] Default value of default logger."""

    def __init__(self, date_fmt=None, default=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_attr("dete_fmt", date_fmt)
        self.init_attr("default", default)

        addLevelName(WARNING, "WARN")
        addLevelName(CRITICAL, "CRIT")
