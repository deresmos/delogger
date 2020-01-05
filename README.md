delogger
==

[![Build Status](https://travis-ci.org/deresmos/delogger.svg?branch=master)](https://travis-ci.org/deresmos/delogger)
[![PyPI](https://badge.fury.io/py/delogger.svg)](https://badge.fury.io/py/delogger)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/deresmos/delogger/blob/master/LICENSE)


Abount
===
Delogger is a Python package that makes easy use of decided logging.

The default logging includes the following:
- Stream handler
- In save mode, log is saved in directory as program execution unit.

### Delogger
- It behaves like normal logging.
- Decorator `Delogger.debuglog` logging arguments and return values

### DeloggerQueue
- Non-blocking logging using QueueHandler.
- Decorator `DeloggerQueue.debuglog` logging arguments and return values


## Settings
TODO

Installation
==
To install Delogger, use pip.

```bash
pip install delogger

```

Examples
==


### Normal stream mode

```python
from delogger import Delogger

delogger = Delogger(name='test_logger')
logger = delogger.logger

logger.info('Start logging')
logger.debug('debug')
logger.warning('warning')
logger.info('End logging')
```

Output
```
Start logging
WARN  2020-01-04 22:59:02 test.py:8 warning
End logging
```


### Debug stream mode

```python
from delogger import Delogger

Delogger.is_debug_stream = True
delogger = Delogger(name='test_logger')
logger = delogger.logger

logger.info('Start logging')
logger.debug('debug')
logger.warning('warning')
logger.info('End logging')
```

Output
```
INFO  2020-01-04 23:00:07 test.py:7 Start logging
DEBUG 2020-01-04 23:00:07 test.py:8 debug
WARN  2020-01-04 23:00:07 test.py:9 warning
INFO  2020-01-04 23:00:07 test.py:10 End logging
```


### Save log file

```python
from delogger import Delogger

Delogger.is_save_file = True
delogger = Delogger(name='test_logger', filepath='%Y/%m%d.log')
logger = delogger.logger

logger.info('Start logging')
logger.debug('debug')
logger.warning('warning')
logger.info('End logging')
```

Output
```
2020-01-04 23:02:13.722 INFO test.py:7 Start logging
2020-01-04 23:02:13.722 DEBUG test.py:8 debug
2020-01-04 23:02:13.722 WARN test.py:9 warning
2020-01-04 23:02:13.722 INFO test.py:10 End logging
```


### Queue mode

```python
import time

from delogger import DeloggerQueue

delogger = DeloggerQueue(name='test_logger')
logger = delogger.logger

print('Start queue mode')
logger.info('Start logging')
logger.debug('debug')
logger.warning('warning')
time.sleep(1)
logger.info('End logging')
print('End queue mode')
```

Output
```
Start queue mode
Start logging
WARN  2020-01-04 23:01:56 test.py:11 warning
End queue mode
End logging
```


### No Color stream mode

```python
from delogger import Delogger

Delogger.is_color_stream = False
delogger = Delogger(name='test_logger')
logger = delogger.logger

logger.info('Start logging')
logger.debug('debug')
logger.warning('warning')
logger.info('End logging')
```

Output
```
Start logging
WARN  2020-01-04 22:59:02 test.py:8 warning
End logging
```


### Debug and no color stream mode

```python
from delogger import Delogger

Delogger.is_color_stream = False
Delogger.is_debug_stream = True
delogger = Delogger(name='test_logger')
logger = delogger.logger

logger.info('Start logging')
logger.debug('debug')
logger.warning('warning')
logger.info('End logging')
```

Output
```
INFO  2020-01-04 23:00:07 test.py:7 Start logging
DEBUG 2020-01-04 23:00:07 test.py:8 debug
WARN  2020-01-04 23:00:07 test.py:9 warning
INFO  2020-01-04 23:00:07 test.py:10 End logging
```
