from delogger import Delogger
from delogger.decorators.debug_log import DebugLog
from delogger.decorators.line_profile import LineProfileStats
from delogger.modes.file import CountRotatingFileMode

if __name__ == "__main__":
    delogger = Delogger()
    delogger.load_modes(
        CountRotatingFileMode(filepath="log/%Y/%Y-%m-%d.log", backup_count=0)
    )
    delogger.load_decorators(DebugLog(), LineProfileStats())

    logger = delogger.get_logger()

    @logger.add_line_profile
    def test():
        logger.debug("debug")
        logger.info("info")
        logger.warning("warn")
        logger.error("error")
        logger.critical("critical")

    for _ in range(2):
        test()
    logger.print_stats()
