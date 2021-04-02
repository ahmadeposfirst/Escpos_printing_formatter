from datetime import datetime
from kivy.clock import Clock
from functools import partial
from backend.date import standard_datetime
import os

class Level:
    def __init__(self, type, value, color):
        self.type = type
        self.value = value
        self.color = color

class LogLevels(object):
    levels = {
        'debug'   : Level(type='[  DEBUG   ]', value=0, color=(0.92, 0.92, 0.92, 1)),
        'info'    : Level(type='[   INFO   ]', value=1, color=(0, 0, 1, 1)         ),
        'warning' : Level(type='[ WARNING  ]', value=2, color=(1, 0.8, 0, 1)       ),
        'error'   : Level(type='[  ERROR   ]', value=3, color=(1, 0, 0, 1)         ),
        'critical': Level(type='[ CRITICAL ]', value=4, color=(1, 0.2, 0.2, 1)     )
    }

class Logger(LogLevels):
    min_log_level = None
    target = None
    curr_level = None

    @classmethod
    def init(cls, min_level='debug', target=None):
        cls.min_log_level = cls.levels[min_level]
        cls.target = target
        cls.curr_level = None

    @classmethod
    def set_target(cls, target):
        cls.target = target

    @classmethod
    def log(cls, log_msg, log_level):
        cls.curr_level = cls.levels[log_level]
        if cls._is_level_allowed():
            cls._write_to_log(msg=log_msg)
            cls._write_to_target(msg=log_msg)

    @classmethod
    def _write_to_log(cls, msg):
        # formats the log string
        msg = f'[{standard_datetime()}] {cls.curr_level.type} {msg}'
        
        # prints the log to console
        print(msg)

        # if logs directory does not exists make one
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # append log to app.log 
        with open(os.path.join('logs', 'app.log'), 'a') as fp:
            fp.write(f'{msg}\n')

    @classmethod
    def _write_to_target(cls, msg):
        if cls.target is not None:
            cls.target.text = msg
            cls.target.color = cls.curr_level.color
            Clock.schedule_once(partial(clear_msg, target), 5)

    @classmethod
    def _is_level_allowed(cls):
        if cls.curr_level.value >= cls.min_log_level.value:
            return True
        cls.curr_level = None
        return False

    def clear_msg(target, obj):
        target.text = ""
