Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
import io
import requests
from django.core.exceptions import ValidationError
from django.test.utils import setup_test_environment, teardown_test_environment
import sys

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

def reproduce_issue():
    setup_test_environment()
    try:
        contents = io.StringIO("." * (1024 * 1024 * 3))
        files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
        req = requests.Request("POST", "http://localhost:8000/", files=files, data={})
        prepared = req.prepare()
        body = prepared.body
        assert isinstance(body, bytes)
        prepared.body = body.replace(b"!", b"\x00")
        session = requests.Session()
        response = session.send(prepared)
        if response.status_code == 500:
            raise AssertionError("Issue is present")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        teardown_test_environment()

if __name__ == "__main__":
    reproduce_issue()
```
This script sets up a Django test environment, sends a request with a file containing a null byte in its filename, and checks if the response status code is 500. If it is, it raises an `AssertionError` with a stack trace of the issue. If any other exception occurs during the execution, it also prints the stack trace and exits with code 1.