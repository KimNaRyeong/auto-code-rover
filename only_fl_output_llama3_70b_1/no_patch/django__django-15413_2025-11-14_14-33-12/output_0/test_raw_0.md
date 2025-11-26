Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import logging
from django.core.handlers.base import BaseHandler
from django.utils.log import configure_logging

configure_logging()

logging.basicConfig(level=logging.DEBUG)

class Middleware:
    def __init__(self, name):
        self.name = name

    def __call__(self, request):
        return None

def test_async_middleware():
    handler = BaseHandler()
    middleware = Middleware("async_payment_middleware")
    with logging.getLogger('django.request').enabled(True):
        with self.assertLogs('django.request', 'DEBUG') as cm:
            handler.load_middleware(middleware)
            response = None  # Not relevant for this test
            assert len(cm.records) == 1, "Expected one log record"
            message = cm.records[0].getMessage()
            assert message.startswith("Synchronous middleware "), f"Expected 'Synchronous middleware ... adapted.' but got {message}"
            assert message.endswith("adapted."), f"Expected '... adapted.' but got {message}"

def main():
    try:
        test_async_middleware()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script sets up a minimal Django environment, defines a synchronous middleware, and tests that the "Synchronous middleware ... adapted" log message is emitted when loading the middleware. If the message is not logged as expected, an `AssertionError` is raised, and the script prints a stack trace of the issue using the provided `print_stacktrace` function.

To run this script, save it to a file named `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.