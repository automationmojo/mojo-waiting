
"""
.. module:: constants
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the Timeout related constants.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


DEFAULT_WAIT_DELAY = 0
DEFAULT_WAIT_INTERVAL = 5
DEFAULT_WAIT_TIMEOUT = 60

MSG_TEMPL_TIME_COMPONENTS = "    timeout={} start_time={}, end_time={} now_time={} time_diff={}"

class TimeoutState:
    TimedOut = -1
    NotStarted = 0
    Tracking = 1
    Completed = 2
    Running = 3
