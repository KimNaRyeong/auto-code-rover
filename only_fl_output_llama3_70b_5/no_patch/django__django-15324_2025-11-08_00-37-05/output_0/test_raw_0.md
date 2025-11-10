Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
import io
import requests
from django.core.exceptions import ValidationError
from django.test.utils import setup_test_environment
from django.test import RequestFactory

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

def reproduce_issue():
    setup_test_environment()
    factory = RequestFactory()

    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
    req = requests.Request("POST", "http://localhost:8000/", files=files, data={})
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\x00")

    request = factory.post('/', data={'docfile': 'bogus.txt!'}, files=files)

    try:
        from django.http import HttpResponse
        from .views import index  # assuming the view is in views.py
        response = index(request)
        assert False, "Expected ValueError to be raised"
    except Exception as e:
        print_stacktrace(e)
        if not isinstance(e, ValidationError) and "embedded null byte" not in str(e):
            raise

if __name__ == "__main__":
    reproduce_issue()
```
This script sets up a Django test environment, creates a request with a file containing a null character in its filename, and sends the request to the `index` view. If no exception is raised or if the exception is not a `ValueError` with the message "embedded null byte", it raises an `AssertionError`. Otherwise, it prints the stack trace of the exception.

To use this script, save it as `reproducer.py` in the root directory of your Django project and run it with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace. If the issue is fixed, it should exit with code 0.