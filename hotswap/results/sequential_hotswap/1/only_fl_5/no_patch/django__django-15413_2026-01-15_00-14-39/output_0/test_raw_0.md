```python
import logging
import os
import django
from django.conf import settings
from django.test import TestCase
from django.core.management import execute_from_command_line

# Define a minimal Django configuration for the test
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='asecretkey',
    MIDDLEWARE=[
        'reproducer.MyCustomMiddleware',
    ],
)

# Define a dummy middleware to test with
class MyCustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Hello, world!')

from django.urls import path
urlpatterns = [
    path('', index),
]

class MiddlewareAdaptationTest(TestCase):
    def test_middleware_adaptation_logging(self):
        with self.assertLogs('django.request', level='DEBUG') as cm:
            response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("Synchronous middleware ... adapted" in record.getMessage() for record in cm.records),
                        "Expected log message 'Synchronous middleware ... adapted' not found.")

# Initialize Django
django.setup()

# Run the test
def run_tests():
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner()
    test_runner.run_tests(['__main__'])

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

if __name__ == '__main__':
    try:
        run_tests()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```

This script sets up a minimal Django project with a custom middleware and a single view. It then runs a test case that sends a request through the middleware and checks the debug logs to ensure the expected message about adapting synchronous middleware is logged.

This script raises an `AssertionError` if the expected log message is not found, printing a stack trace to help diagnose why the test failed. This behavior will occur when the issue described is present, and the script should exit with code 0 when the issue is fixed, assuming the fix ensures the log message is correctly produced.