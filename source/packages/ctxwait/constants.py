
"""
.. module:: constants
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the TimeoutContext object and very generic constants.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


DEFAULT_WAIT_DELAY = 0
DEFAULT_WAIT_INTERVAL = 5
DEFAULT_WAIT_TIMEOUT = 60

DEFAULT_WHATFOR_TEMPLATE = "Timeout waiting for {}"

MSG_TEMPL_TIME_COMPONENTS = "    timeout={} start_time={}, end_time={} now_time={} time_diff={}"

class TimeoutState:
    TimedOut = -1
    NotStarted = 0
    Tracking = 1
    Completed = 2
    Running = 3
