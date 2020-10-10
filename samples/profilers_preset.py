from delogger.preset.profiler import logger

if __name__ == "__main__":

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

    @logger.line_profile
    def test2():
        logger.debug("debug")

    @logger.memory_profile
    def test3():
        logger.debug("debug")

    @logger.line_memory_profile
    def test4():
        logger.debug("debug")

    test2()
    test3()
    test4()
