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
| is_stream       | If False, disabled stream output           | True                |
| backup_count    | logfile backup_count                       | 5                   |


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
![normal](https://user-images.githubusercontent.com/27688389/49737427-335e1100-fcd0-11e8-8a59-7d0fe3088273.png "normal")


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
![debug](https://user-images.githubusercontent.com/27688389/49737352-03af0900-fcd0-11e8-8420-f1fc295394c8.png "debug")


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
![logfile](https://user-images.githubusercontent.com/27688389/49738444-c730dc80-fcd2-11e8-9fb2-2bd0336e25db.png "logfile")


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
![queue](https://user-images.githubusercontent.com/27688389/49737371-10336180-fcd0-11e8-84dd-f9be5f223f42.png "queue")


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
![no-color-normal](https://user-images.githubusercontent.com/27688389/48709759-c49a1480-ec49-11e8-92ee-99dae12c6e63.png "no-color-normal")


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
![no-color-debug](https://user-images.githubusercontent.com/27688389/49737616-a8314b00-fcd0-11e8-8d11-2274bb7e0ae1.png "no-color-debug")
