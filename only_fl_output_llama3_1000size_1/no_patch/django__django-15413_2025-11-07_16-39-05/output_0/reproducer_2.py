import os
import sys
from django.core.handlers.base import BaseHandler
from unittest import TestCase

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Reproducer(TestCase):
    def test_reproducer(self):
        settings = {'DEBUG': True, 'MIDDLEWARE': ['middleware_exceptions.middleware.async_payment_middleware']}
        handler = BaseHandler()
        handler.adapt_method_mode(True, lambda: None, debug=settings['DEBUG'], name='middleware')
        with self.assertLogs('django.request', 'DEBUG') as cm:
            pass
        if not any(record.getMessage() == "Synchronous middleware ... adapted." for record in cm.records):
            raise AssertionError("Expected log message not found")
        else:
            print("Issue reproduced")

if __name__ == "__main__":
    try:
        Reproducer().test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue fixed")
        sys.exit(0)
