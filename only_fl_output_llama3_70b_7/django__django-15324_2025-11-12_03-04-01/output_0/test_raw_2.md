Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
# reproducer.py

import io
import requests
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.test.utils import setup_test_environment

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
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
    req = requests.Request("POST", "http://localhost:8000/", files=files)
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\x00")
    
    try:
        s = requests.Session()
        response = s.send(prepared)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        if "embedded null byte" in str(e):
            print_stacktrace(e)
            raise AssertionError("ValueError with 'embedded null byte' message was raised")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_file_upload()
```
This script uses the `requests` library to create a request object and send it to a Django server. The `test_file_upload` function is designed to raise an `AssertionError` if the issue is present, with a stack trace of the error. If the issue is fixed, the script will exit with code 0.

To run this script, save it as `reproducer.py` in the root directory of your Django project and execute it with `python3 reproducer.py`. Make sure to start the Django development server before running the script.