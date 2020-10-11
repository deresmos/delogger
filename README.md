# delogger

[![PyPI](https://badge.fury.io/py/delogger.svg)](https://badge.fury.io/py/delogger)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/deresmos/delogger/blob/master/LICENSE)
![test](https://github.com/deresmos/delogger/workflows/Python%20Test/badge.svg)
![CodeQL](https://github.com/deresmos/delogger/workflows/CodeQL/badge.svg)

## About

Delogger is a Python package that makes easy use of decided logging.

### Delogger

- It behaves like normal logging.

### DeloggerQueue

- Non-blocking logging using QueueHandler.

## Installation

To install Delogger, use pip.

```bash
pip install delogger

```

## Sample

### Debug stream and output log

```python
from delogger.presets.debug import logger

if __name__ == "__main__":
    logger.debug("debug msg")
    logger.info("info msg")
    logger.warning("warn msg")
    logger.error("error msg")
    logger.critical("critical msg")
```

Output
![debug_sample_output]()

File output (./log/20201010_164622.log)
```
2020-10-10 16:46:22.050 DEBUG debug_preset.py:4 <module> debug msg
2020-10-10 16:46:22.050 INFO debug_preset.py:5 <module> info msg
2020-10-10 16:46:22.051 WARN debug_preset.py:6 <module> warn msg
2020-10-10 16:46:22.051 ERROR debug_preset.py:7 <module> error msg
2020-10-10 16:46:22.051 CRIT debug_preset.py:8 <module> critical msg
```


and more [samples](https://github.com/deresmos/delogger/tree/main/tests)

## Preset

- `debug`: Output color debug log and save log file.
- `debug_stream`: Output color debug log.
- `output`: Save log file and notify to slack.
- `profiler`: Same debug preset and seted profiles decorator.

## Mode

- `CountRotatingFileMode`: Backup count rotating.
- `TimedRotatingFileMode`: Same logging.handlers.TimedRotatingFileHandler.
- `SlackWebhookMode`: Log to slack. (Incomming webhook)
- `SlackTokenMode`: Log to slack. (token key)
- `StreamColorDebugMode`: Output color log. (debug and above)
- `StreamDebugMode`: Output noncolor log. (debug and above)
- `StreamInfoMode`: Output noncolor log. (info and above)
- `PropagateMode`: Set Setropagate true.

## Environment

- `DELOGGER_NAME`: logger name for presets.
- `DELOGGER_FILEPATH`: output log filepath for presets.
- `DELOGGER_SLACK_WEBHOOK`: send slack for presets.

## Decorator

Inject decorator into logger.

### debuglog

```text
DEBUG 21:00:00 debug_log.py:32 START test args=('test',) kwargs={}
DEBUG 21:00:01 debug_log.py:39 END test return=value
```

### line_profile

Required [line_profiler](https://github.com/pyutils/line_profiler) package.

```text
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

Required [memory_profiler](https://github.com/pythonprofilers/memory_profiler) package.

```text
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

Required [line_profiler](https://github.com/pyutils/line_profiler) and [memory_profiler](https://github.com/pythonprofilers/memory_profiler) package.

```text
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

Required [line_profiler](https://github.com/pyutils/line_profiler) package.

```text
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
