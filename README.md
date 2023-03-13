# Contextual Waiting Module - contextualwaiting

This package provides support for enhanced context based waiting.  The waiting code
patterns used are designed to present the best results in test stacktraces presented
when a wait fails.

..code-block:: python

    from ctxwait import WaitContext, wait_for_it

    def some_wait_helper(wctx: WaitContext):
        finished = False

        // TODO: Check if something is finished

        if not finished and wctx.final_attempt:
            toerr = wctx.create_timeout("Test timeout")
        
        return finished

    wait_for_it(some_wait_helper)

The `wait_for_it` method has many different parameters that can be used to override the
behavior of the wait loop.

..code-block:: python

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

The `wait_for_it` function must be passed a method that follows the `WaitCallback` protocol.  The function
can have variable arguments and keyword arguements but the first parameter to the `WaitCallback` method
must be a `WaitContext` object.


