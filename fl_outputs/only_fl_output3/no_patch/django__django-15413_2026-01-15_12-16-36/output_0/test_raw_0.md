```python
# reproducer.py
import logging
import sys
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.management import execute_from_command_line
from django.urls import path
from django.http import HttpResponse


# Define a dummy view
def dummy_view(request):
    return HttpResponse('Hello, World')


# Define synchronous middleware
class SyncMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


# Define settings dynamically
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='asecrettoeverybody',
    MIDDLEWARE=[
        'reproducer.SyncMiddleware',
    ],
)

# Dummy URL Patterns
urlpatterns = [
    path('test/', dummy_view, name='dummy_view'),
]

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_log_message():
    try:
        logger = logging.getLogger('django.request')
        logger.setLevel(logging.DEBUG)
        stream = logging.StreamHandler()
        logger.addHandler(stream)
        handler = WSGIHandler()

        # Make a mock request
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/test/',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': '80',
            'wsgi.input': '',
            'wsgi.url_scheme': 'http',
        }
        handler(environ, lambda *args, **kwargs: None)

        log_output = stream.stream.getvalue()
        expected_message = "Synchronous middleware reproducer.SyncMiddleware adapted."
        assert expected_message in log_output, "Expected log message not found."

    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        check_log_message()
    except AssertionError:
        sys.exit(1)
    else:
        print("Issue not present, exiting with code 0.")
        sys.exit(0)
```

This script is designed to dynamically configure a Django environment, introduce a simple synchronous middleware, and assert that the expected debug log message regarding the adaptation of synchronous middleware is present. It will print a stack trace if the assertion fails, indicating the issue is present. If the expected behavior is observed (i.e., the issue is fixed), it will exit with a 0 code, showing everything works as expected. This script needs Django to be installed in the environment where it is executed.