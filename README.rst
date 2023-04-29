=============================================
Automation Mojo Waiting Module - mojo-waiting
=============================================

This package provides support for enhanced context based waiting.  The waiting code
patterns used are designed to present the best results in test stacktraces presented
when a wait fails.  This makes the `mojo.waiting` module perfect for use with
test frameworks such as `pytest` and `testplus` that show code context in the error
report stack traces.

Another important aspect of the `mojo.waiting` module is that it uses `datetime`
timestamps and `timespan` for lengths of time so timeouts in error reporting are easier
to interpret.

```
    Traceback (most recent call last):
    File "/home/myron/repos/mojo.waiting/source/tests/test_wait_for_it.py", line 97, in test_basic_wait_for_it_timeout
        future.result()
    File "/usr/lib/python3.10/concurrent/futures/_base.py", line 451, in result
        return self.__get_result()
    File "/usr/lib/python3.10/concurrent/futures/_base.py", line 403, in __get_result
        raise self._exception
    File "/usr/lib/python3.10/concurrent/futures/thread.py", line 58, in run
        result = self.fn(*self.args, **self.kwargs)
    File "/home/myron/repos/mojo.waiting/source/tests/test_wait_for_it.py", line 88, in wait_task
        ctxwait.wait_for_it(wait_helper, interval=.5, timeout=2)
    File "/home/myron/repos/mojo.waiting/source/packages/ctxwait/waiting.py", line 103, in wait_for_it
        raise toerr
    TimeoutError: Timeout waiting for 'wait_helper':
        timeout=2 start_time=2023-03-13 14:57:29.860302, end_time=2023-03-13 14:57:31.860302 now_time=2023-03-13 14:57:31.863681 time_diff=0:00:02.003379
```

The following is an example of how the `mojo.waiting` module is used.

```{python}

    from ctxwait import WaitContext, wait_for_it

    def some_wait_helper(wctx: WaitContext):
        finished = False

        // TODO: Check if something is finished, the code and variables used
        //       here will show up in any tracebacks from pytest or testplus
        //       because the timeout is being raised in the appropriate scope.

        if not finished and wctx.final_attempt:
            whatfor = "Test timeout"
            toerr = wctx.create_timeout(whatfor)
            raise toerr

        return finished

    wait_for_it(some_wait_helper)
```

The `wait_for_it` method has many different parameters that can be used to override the
behavior of the wait loop.

```{python}

    def wait_for_it(looper: WaitCallback, *largs, what_for: Optional[str]=None, delay: float=DEFAULT_WAIT_DELAY,
                interval: float=DEFAULT_WAIT_INTERVAL, timeout: float=DEFAULT_WAIT_TIMEOUT,
                lkwargs: Dict[Any, Any]={}, wctx: Optional[WaitContext]=None):
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
        ...
```

The `wait_for_it` function must be passed a method that follows the `WaitCallback` protocol.  The function
can have variable arguments and keyword arguements but the first parameter to the `WaitCallback` method
must be a `WaitContext` object.


