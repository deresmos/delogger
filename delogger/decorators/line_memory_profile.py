from typing import Generator
from typing import List
from typing import Tuple

from delogger.decorators.base import DecoratorBase
from delogger.util.warn import warn_import

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from line_profiler import LineProfiler

    _can_line_profiler = True
except ImportError:  # pragma: no cover
    _can_line_profiler = False


try:
    from memory_profiler import profile

    _can_memory_profiler = True
except ImportError:  # pragma: no cover
    _can_memory_profiler = False


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

    def can_run(self) -> bool:
        if not _can_line_profiler:
            warn_import(self.decorator_name, "line_profiler")
            return False

        if not _can_memory_profiler:
            warn_import(self.decorator_name, "memory_profiler")
            return False

        return True

    def wrapper(self, f, *args, **kwargs):
        # memory_profiler
        with StringIO() as s:
            rtn = profile(f, stream=s, precision=2)(*args, **kwargs)
            memory_value = self._memory_profiler_parse(s.getvalue())

        # line_profiler
        prof = LineProfiler()
        prof.add_function(f)

        rtn = prof.runcall(f, *args, **kwargs)
        with StringIO() as s:
            prof.print_stats(stream=s)
            mix, line_tmp = self._line_profiler_parse(s.getvalue())

        # memory line mix output
        template = self.L_M_TEMPLATE
        for l, m in zip(line_tmp, memory_value):
            l_m_mix = l[:5] + m
            mix.append(template.format(*l_m_mix))
        mix[self.L_M_HEADER_INDEX] = template.format(*self.L_M_HEADER)
        mix[self.L_M_SEPARATOR_INDEX] += "=" * 27
        self.logger.debug("line, memory profiler result\n" + "\n".join(mix))

        return rtn

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
