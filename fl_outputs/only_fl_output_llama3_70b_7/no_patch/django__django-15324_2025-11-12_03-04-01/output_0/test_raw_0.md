Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
# reproducer.py

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

def test_file_upload():
    setup_test_environment()
    factory = RequestFactory()

    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
    req = factory.post("/", files=files)
    
    try:
        from django.http import HttpRequest
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {}
        request.FILES = files
        from . import views  # assuming the view is in the same package
        response = views.index(request)
        assert False, "Expected ValueError to be raised"
    except ValidationError as e:
        print_stacktrace(e)
        raise AssertionError("ValidationError should not be raised")
    except ValueError as e:
        if "embedded null byte" not in str(e):
            print_stacktrace(e)
            raise AssertionError("Expected ValueError with 'embedded null byte' message")

if __name__ == "__main__":
    test_file_upload()
```
This script uses the `RequestFactory` from Django's testing framework to create a request object, and then calls the `index` view function directly. The `test_file_upload` function is designed to raise an `AssertionError` if the issue is present, with a stack trace of the error. If the issue is fixed, the script will exit with code 0.

To run this script, save it as `reproducer.py` in the root directory of your Django project and execute it with `python3 reproducer.py`.