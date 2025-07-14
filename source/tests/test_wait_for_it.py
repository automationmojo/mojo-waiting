
import unittest

import concurrent.futures
import time
import traceback

from mojo.waiting.constants import DEFAULT_WAIT_TIMEOUT, DEFAULT_WAIT_INTERVAL
from mojo.waiting.waitfunction import wait_for_it
from mojo.waiting.waitmodel import WaitContext

class TestWaitForIt(unittest.TestCase):

    def test_basic_wait_for_it(self):
        finished = False

        with concurrent.futures.ThreadPoolExecutor() as pool:
            
            def wait_task():

                def wait_helper(wctx: WaitContext):
                    success = finished
                    if not success:
                        print("test_basic_wait_for_it: still waiting")

                    return success

                wait_for_it(wait_helper)

                return
            
            future = pool.submit(wait_task)

            time.sleep(DEFAULT_WAIT_INTERVAL * 2)

            finished = True

            concurrent.futures.wait([future], DEFAULT_WAIT_TIMEOUT)

        return

    def test_basic_wait_for_it_final_attempt(self):
        final_attempt_triggered = False

        with concurrent.futures.ThreadPoolExecutor() as pool:
            
            def wait_task():

                def wait_helper(wctx: WaitContext):
                    nonlocal final_attempt_triggered

                    success = False
                    if not success and wctx.final_attempt:
                        final_attempt_triggered = wctx.final_attempt
                        success = True

                    return success

                wait_for_it(wait_helper, interval=.5, timeout=2)

                return
            
            future = pool.submit(wait_task)

            concurrent.futures.wait([future], DEFAULT_WAIT_TIMEOUT)
        
        self.assertTrue(final_attempt_triggered, "The final_attempt should have been triggered.")

        return
    
    def test_basic_wait_for_it_timeout(self):
        final_attempt_triggered = False
        timeout_raised = False

        with concurrent.futures.ThreadPoolExecutor() as pool:
            
            def wait_task():

                def wait_helper(wctx: WaitContext):
                    nonlocal final_attempt_triggered

                    success = False
                    if not success and wctx.final_attempt:
                        final_attempt_triggered = wctx.final_attempt
                        wctx.create_timeout("Test timeout")

                    return success

                wait_for_it(wait_helper, interval=.5, timeout=2)

                return
            
            future = pool.submit(wait_task)

            concurrent.futures.wait([future], DEFAULT_WAIT_TIMEOUT)
        
        try:
            future.result()
        except TimeoutError as toerr:
            errmsg = traceback.format_exc()
            timeout_raised = True
        
        self.assertTrue(timeout_raised, "A 'TimeoutError' should have been raised.")

        return


if __name__ == '__main__':
    unittest.main()
