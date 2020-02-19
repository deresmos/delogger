delogger
==

[![Build Status](https://travis-ci.org/deresmos/delogger.svg?branch=master)](https://travis-ci.org/deresmos/delogger)
[![PyPI](https://badge.fury.io/py/delogger.svg)](https://badge.fury.io/py/delogger)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/deresmos/delogger/blob/master/LICENSE)


Abount
===
Delogger is a Python package that makes easy use of decided logging.

### Delogger
- It behaves like normal logging.

### DeloggerQueue
- Non-blocking logging using QueueHandler.


Installation
==
To install Delogger, use pip.

```bash
pip install delogger

```

Example
==

### Example1
```python
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
```

Output:
```
DEBUG 22:16:01 debug.py:13 debug
INFO  22:16:01 debug.py:14 info
WARN  22:16:01 debug.py:15 warn
ERROR 22:16:01 debug.py:16 error
CRIT  22:16:01 debug.py:17 critical
```

File output (./log/20200219_221601.log)
```
2020-02-19 22:16:01.320 DEBUG debug.py:13 debug
2020-02-19 22:16:01.320 INFO debug.py:14 info
2020-02-19 22:16:01.320 WARN debug.py:15 warn
2020-02-19 22:16:01.320 ERROR debug.py:16 error
2020-02-19 22:16:01.320 CRIT debug.py:17 critical
```

Same `debug` preset.
```python
from delogger.presets.debug import logger

if __name__ == "__main__":
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning("WARN")
    logger.error("ERROR")
    logger.critical("CRITICAL")
```

### Example2
```python
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
```


File output (log/2020/2020-02-19.log)
```
2020-02-19 23:01:01.921 DEBUG debug.py:17 debug
2020-02-19 23:01:01.921 INFO debug.py:18 info
2020-02-19 23:01:01.922 WARN debug.py:19 warn
2020-02-19 23:01:01.922 ERROR debug.py:20 error
2020-02-19 23:01:01.922 CRIT debug.py:21 critical
2020-02-19 23:01:01.922 DEBUG debug.py:17 debug
2020-02-19 23:01:01.922 INFO debug.py:18 info
2020-02-19 23:01:01.922 WARN debug.py:19 warn
2020-02-19 23:01:01.922 ERROR debug.py:20 error
2020-02-19 23:01:01.922 CRIT debug.py:21 critical
2020-02-19 23:01:01.935 DEBUG line_profile.py:67 line_profiler_stats result
Timer unit: 1e-06 s

Total time: 0.000871 s
File: examples/debug.py
Function: test at line 15

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    15                                               @logger.add_line_profile
    16                                               def test():
    17         2        267.0    133.5     30.7          logger.debug("debug")
    18         2        165.0     82.5     18.9          logger.info("info")
    19         2        148.0     74.0     17.0          logger.warning("warn")
    20         2        148.0     74.0     17.0          logger.error("error")
    21         2        143.0     71.5     16.4          logger.critical("critical")
```

Preset
==
- `debug`: Output color debug log and save log file.
- `debug_stream`: Output color debug log.
- `output`: Save log file and notify to slack.
- `profiler`: Same debug preset and seted profiles decorator.

Mode
==
- `CountRotatingFileMode`: Backup count rotating.
- `TimedRotatingFileMode`: Same logging.handlers.TimedRotatingFileHandler.
- `SlackWebhookMode`: Log to slack. (Incomming webhook)
- `SlackTokenMode`: Log to slack. (token key)
- `StreamColorDebugMode`: Output color log. (debug and above)
- `StreamColorInfoMode`: Output color log. (info and above)
- `StreamDebugMode`: Output noncolor log. (debug and above)
- `StreamInfoMode`: Output noncolor log. (info and above)
- `PropagateMode`: Set Setropagate true.

Decorator
==
Inject decorator into logger.

### debuglog

```
DEBUG 21:00:00 debug_log.py:32 START test args=('test',) kwargs={}
DEBUG 21:00:01 debug_log.py:39 END test return=value
```

### line_profile

```
DEBUG 21:38:22 line_profile.py:28 line_profiler result
Timer unit: 1e-06 s

Total time: 6.4e-05 s
File: test.py
Function: test at line 6

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     6                                           @logger.line_profile
     7                                           def test(arg1):
     8       101         43.0      0.4     67.2      for i in range(100):
     9       100         21.0      0.2     32.8          pass
    10         1          0.0      0.0      0.0      return i
```

### memory_profile

```
DEBUG 21:40:31 memory_profile.py:25 memory_profiler result
Filename: test.py

Line #    Mem usage    Increment   Line Contents
================================================
     6    37.96 MiB    37.96 MiB   @logger.memory_profile
     7                             def test(arg1):
     8    45.43 MiB     7.47 MiB       a = [0] * 1000 * 1000
     9    45.43 MiB     0.00 MiB       for i in range(100):
    10    45.43 MiB     0.00 MiB           pass
    11    45.43 MiB     0.00 MiB       return i
```

### line_memory_profile

```
DEBUG 21:41:08 line_memory_profile.py:70 line, memory profiler result
Timer unit: 1e-06 s

Total time: 0.004421 s
File: test.py
Function: test at line 6

Line #      Hits         Time  Per Hit   % Time    Mem usage    Increment   Line Contents
=========================================================================================
     6                                             37.96 MiB    37.96 MiB   @logger.line_memory_profile
     7                                                                      def test(arg1):
     8         1       4355.0   4355.0     98.5    45.43 MiB     7.47 MiB       a = [0] * 1000 * 1000
     9       101         33.0      0.3      0.7    45.43 MiB     0.00 MiB       for i in range(100):
    10       100         32.0      0.3      0.7    45.43 MiB     0.00 MiB           pass
    11         1          1.0      1.0      0.0    45.43 MiB     0.00 MiB       return i
```

### add_line_profile
- It can adjust the timing of profile output

```
DEBUG 21:45:55 line_profile.py:67 line_profiler_stats result
Timer unit: 1e-06 s

Total time: 0.009081 s
File: test.py
Function: test at line 6

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     6                                           @logger.add_line_profile
     7                                           def test(arg1):
     8         2       8957.0   4478.5     98.6      a = [0] * 1000 * 1000
     9       202         71.0      0.4      0.8      for i in range(100):
    10       200         52.0      0.3      0.6          pass
    11         2          1.0      0.5      0.0      return i
```
