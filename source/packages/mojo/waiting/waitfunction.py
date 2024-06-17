"""
.. module:: waitfunction
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the wait_for_it function.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from typing import Any, Dict, Optional

import time


from mojo.waiting.constants import (
    DEFAULT_WAIT_DELAY,
    DEFAULT_WAIT_INTERVAL,
    DEFAULT_WAIT_TIMEOUT
)


from mojo.waiting.waitmodel import WaitCallback, WaitContext


def wait_for_it(looper: WaitCallback, *largs, what_for: Optional[str]=None, delay: float=DEFAULT_WAIT_DELAY,
                interval: float=DEFAULT_WAIT_INTERVAL, timeout: float=DEFAULT_WAIT_TIMEOUT,
                lkwargs: Optional[Dict[Any, Any]]=None, wctx: Optional[WaitContext]=None):
    """
        Provides for convenient mechanism to wait for criteria to be met before proceeding.

        :param looper: A callback method that is repeatedly called while it returns `False` up-to
                       the end of a timeout period, and that will return `True` if a waited on
                       condition is met prior to a timeout condition being met.
        :param largs: Arguements to pass to the looper callback function.
        :param what_for: A breif description of what is being waited for.
        :param delay: An initial time delay to consume before beginning the waiting process.
        :param interval: A period of time to delay between rechecks of the wait conditon
        :param timeout: The maximum period of time in seconds that should be waited before timing out.
        :param lkwargs: Additional keyword arguments to pass to the looper function

        :raises TimeoutError: A timeout error with details around the wait condition.

        ..note: The 'delay', 'interval' and 'timeout' parameters will be ignored if the 'wctx' parameter
                is passed as the wctx (WaitContext) parameter includes these values with it.
    """

    if lkwargs is None:
        lkwargs = {}

    if what_for is None:
        what_for = "'{}'".format(looper.__name__)

    if wctx is None:
        wctx = WaitContext(timeout, interval=interval, delay=delay, what_for=what_for)

    if wctx.delay > 0:
        time.sleep(DEFAULT_WAIT_DELAY)

    wctx.mark_begin()

    condition_met = False

    while True:
        condition_met = looper(wctx, *largs, **lkwargs)
        if condition_met:
            wctx.mark_complete()
            break

        if not wctx.should_continue():
            break

        if wctx.interval > 0:
            time.sleep(wctx.interval)

    if not condition_met:
        # Mark the time we are performing the final attempt
        wctx.mark_time()
        wctx.mark_final_attempt()
        condition_met = looper(wctx, *largs, **lkwargs)

    if not condition_met:
        toerr = wctx.create_timeout(what_for)
        raise toerr

    wctx.mark_complete()

    return



