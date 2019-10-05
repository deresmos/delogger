from delogger.base import DeloggerBase

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from line_profiler import LineProfiler
except ImportError:
    pass

try:
    from memory_profiler import profile
except ImportError:
    pass


class LineEmpty(Exception):
    pass


class DeloggerDebugLogDecorator(DeloggerBase):
    @classmethod
    def debuglog(cls, func):
        """When this decorator is set, the argument and return value are out-
        put to the log.
        """

        logger = cls(name="_debugger").logger

        def wrapper(*args, **kwargs):
            # Output function name and argument.
            msg = "START {} args={} kwargs={}".format(func.__qualname__, args, kwargs)
            logger.debug(msg)

            # Output function name and return value.
            rtn = func(*args, **kwargs)
            msg = "END {} return={}".format(func.__qualname__, rtn)
            logger.debug(msg)

            return rtn

        return wrapper


class DeloggerLineProfilerDecorator(DeloggerBase):
    @classmethod
    def line_profiler(cls, func):
        """line_profiler are output to the log.
        """

        logger = cls(name="_debugger_l").logger

        def wrapper(*args, **kwargs):
            # output line_profiler
            prof = LineProfiler()
            prof.add_function(func)

            rtn = prof.runcall(func, *args, **kwargs)
            with StringIO() as f:
                prof.print_stats(stream=f)
                msg = "line_profiler result\n{}".format(f.getvalue())
            logger.debug(msg)

            return rtn

        return wrapper


class DeloggerMemoryProfilerDecorator(DeloggerBase):
    @classmethod
    def memory_profiler(cls, func):
        """memory_profiler are output to the log.
        """

        logger = cls(name="_debugger_m").logger

        def wrapper(*args, **kwargs):
            # output memory_profiler
            with StringIO() as f:
                rtn = profile(func, stream=f, precision=2)(*args, **kwargs)
                msg = "memory_profiler result\n{}".format(f.getvalue())
            logger.debug(msg)

            return rtn

        return wrapper


class DeloggerLineMemoryProfilerDecorator(DeloggerBase):
    L_M_HEADER_INDEX = 6
    L_M_SEPARATOR_INDEX = 7
    L_M_TEMPLATE = "{0:>6} {1:>9} {2:>12} {3:>8} {4:>8} " "{5:>12} {6:>12}   {7:<}"
    L_M_HEADER = [
        "Line #",
        "Hits",
        "Time",
        "Per Hit",
        "% Time",
        "Mem usage",
        "Increment",
        "Line Contents",
    ]

    @classmethod
    def line_memory_profiler(cls, func):
        """line_profiler and memory_profiler mix are output to the log.
        """

        logger = cls(name="_debugger_l_m").logger

        def wrapper(*args, **kwargs):
            # memory_profiler
            with StringIO() as f:
                rtn = profile(func, stream=f, precision=2)(*args, **kwargs)
                memory_value = cls._memory_profiler_parse(f.getvalue())

            # line_profiler
            prof = LineProfiler()
            prof.add_function(func)

            rtn = prof.runcall(func, *args, **kwargs)
            with StringIO() as f:
                prof.print_stats(stream=f)
                mix, line_tmp = cls._line_profiler_parse(f.getvalue())

            # memory line mix output
            template = cls.L_M_TEMPLATE
            for l, m in zip(line_tmp, memory_value):
                l_m_mix = l[:5] + m
                mix.append(template.format(*l_m_mix))
            mix[cls.L_M_HEADER_INDEX] = template.format(*cls.L_M_HEADER)
            mix[cls.L_M_SEPARATOR_INDEX] += "=" * 27
            logger.debug("line, memory profiler result\n" + "\n".join(mix))

            return rtn

        return wrapper

    @staticmethod
    def _memory_profiler_parse(result):
        for line in result.split("\n"):
            try:
                elem = line.split()
                if not elem:
                    continue

                lineno = elem[0].isnumeric()
                if not lineno:
                    continue

                contents = line[35:]
                if len(elem) < 2:
                    raise LineEmpty()
                float(elem[1])

                mem = elem[1:3]
                inc_mem = elem[3:5]
                yield [" ".join(mem), " ".join(inc_mem), contents]

            except ValueError:
                yield ["", "", contents]
                continue
            except LineEmpty:
                yield ["", "", ""]
                continue

    @staticmethod
    def _line_profiler_parse(result):
        mix = []
        line_tmp = []
        for line in result.split("\n"):
            try:
                elem = line.split()
                if not elem:
                    mix.append(line)
                    continue

                is_lineno = elem[0].isnumeric()
                if not is_lineno:
                    mix.append(line)
                    continue

                if len(elem) < 2:
                    raise LineEmpty()
                float(elem[1])
                line_tmp.append(elem[:5])

            except ValueError:
                line_tmp.append([elem[0], "", "", "", ""])
                continue
            except LineEmpty:
                line_tmp.append([elem[0], "", "", "", ""])
                continue

        for _ in range(5):
            if not mix[-1]:
                del mix[-1]
            else:
                break

        return mix, line_tmp


class DeloggerDecorators(
    DeloggerDebugLogDecorator,
    DeloggerLineProfilerDecorator,
    DeloggerMemoryProfilerDecorator,
    DeloggerLineMemoryProfilerDecorator,
):
    pass
