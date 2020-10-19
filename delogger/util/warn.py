import warnings


def warn_import(decorator, package):
    _warn(
        f"Not work correctory {decorator} decorator. Please install {package} package."
    )


def _warn(msg):
    warnings.warn(msg, ImportWarning)
