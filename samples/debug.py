from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.modes.file import CountRotatingFileMode
from delogger.modes.stream import StreamColorDebugMode

if __name__ == "__main__":
    delogger = Delogger()
    delogger.load_modes(StreamColorDebugMode(), CountRotatingFileMode())
    delogger.load_decorators(DebugLog())

    logger = delogger.get_logger()

    logger.debug("debug")
    logger.info("info")
    logger.warning("warn")
    logger.error("error")
    logger.critical("critical")
