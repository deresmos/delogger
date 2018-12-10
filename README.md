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
| variable name   | description                                | default             |
| -------------   | -------------                              | ------              |
| date_fmt        | date and time format                       | '%Y-%m-%d %H:%M:%S' |
| stream_level    | Stream level                               | logging.INFO        |
| file_level      | Level of file output                       | logging.DEBUG       |
| is_save_file    | whether to save the log file               | False               |
| is_color_stream | whether to make the stream color output    | False               |
| is_debug_stream | Whether to output the stream in debug mode | False               |
| default         | Whether to use the default handler         | True                |
| dirpath         | log output folder                          | 'log'               |
| filepath        | log output filepath                        | None                |


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
![sample3](https://user-images.githubusercontent.com/27688389/48709824-fad79400-ec49-11e8-8a93-a5c72bdec5fc.png "sample3")


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
![sample2](https://user-images.githubusercontent.com/27688389/48709786-d8de1180-ec49-11e8-919b-31b9f7a51bfc.png "sample2")


### Color stream mode

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
![sample1](https://user-images.githubusercontent.com/27688389/48709759-c49a1480-ec49-11e8-92ee-99dae12c6e63.png "sample1")


### Debug and color stream mode

```python
from delogger import Delogger

Delogger.is_color_stream = True
Delogger.is_debug_stream = True
delogger = Delogger(name='test_logger')
logger = delogger.logger

logger.info('Start logging')
logger.debug('debug')
logger.warning('warning')
logger.info('End logging')
```
![sample4](https://user-images.githubusercontent.com/27688389/48709860-117deb00-ec4a-11e8-905f-7f1597363c38.png "sample4")


### Save log file

```python
from delogger import Delogger

Delogger.is_save_file = True
delogger = Delogger(name='test_logger')
logger = delogger.logger

logger.info('Start logging')
logger.debug('debug')
logger.warning('warning')
logger.info('End logging')
```
![sample5](https://user-images.githubusercontent.com/27688389/48978687-b426e580-f0f2-11e8-8b4c-fa418471e576.png "sample5")


### Queue mode

```python
import time

from delogger import DeloggerQueue

DeloggerQueue.is_color_stream = True
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
![sample6](https://user-images.githubusercontent.com/27688389/48709874-1e024380-ec4a-11e8-818f-521260c9c4e9.png "sample6")
