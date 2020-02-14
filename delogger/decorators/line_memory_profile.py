from typing import Callable, Generator, List, Tuple

from delogger.decorators.base import DecoratorBase

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


class LineMemoryProfile(DecoratorBase):
    decorator_name = "line_memory_profile"

    L_M_HEADER_INDEX: int = 6
    L_M_SEPARATOR_INDEX: int = 7
    L_M_TEMPLATE: str = "{0:>6} {1:>9} {2:>12} {3:>8} {4:>8} " "{5:>12} {6:>12}   {7:<}"
    L_M_HEADER: List[str] = [
        "Line #",
        "Hits",
        "Time",
        "Per Hit",
        "% Time",
        "Mem usage",
        "Increment",
        "Line Contents",
    ]

    def decorator(self, func) -> Callable:
        """When this decorator is set, the argument and return value are out-
        put to the log.
        """

        def wrapper(*args, **kwargs):
            # memory_profiler
            with StringIO() as f:
                rtn = profile(func, stream=f, precision=2)(*args, **kwargs)
                memory_value = self._memory_profiler_parse(f.getvalue())

            # line_profiler
            prof = LineProfiler()
            prof.add_function(func)

            rtn = prof.runcall(func, *args, **kwargs)
            with StringIO() as f:
                prof.print_stats(stream=f)
                mix, line_tmp = self._line_profiler_parse(f.getvalue())

            # memory line mix output
            template = self.L_M_TEMPLATE
            for l, m in zip(line_tmp, memory_value):
                l_m_mix = l[:5] + m
                mix.append(template.format(*l_m_mix))
            mix[self.L_M_HEADER_INDEX] = template.format(*self.L_M_HEADER)
            mix[self.L_M_SEPARATOR_INDEX] += "=" * 27
            self.logger.debug("line, memory profiler result\n" + "\n".join(mix))

            return rtn

        return wrapper

    @staticmethod
    def _memory_profiler_parse(result) -> Generator[List[str], None, None]:
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
    def _line_profiler_parse(result) -> Tuple[List[str], List[List[str]]]:
        mix: List[str] = []
        line_tmp: List[List[str]] = []
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
