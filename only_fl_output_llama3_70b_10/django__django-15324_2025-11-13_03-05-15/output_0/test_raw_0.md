Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
#!/usr/bin/env python3

import io
import requests
from django.http import HttpResponse, HttpRequest
from django.core.handlers.wsgi import WSGIRequest

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

def test_upload_file():
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
    req = requests.Request("POST", "http://localhost:8000/", files=files, data={})
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\x00")
    try:
        requests.Session().send(prepared)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    test_upload_file()
```
This script sends a POST request to `http://localhost:8000/` with a file upload containing a null character in the filename. If the issue is present, it will raise an `AssertionError` and print the stack trace of the exception. If the issue is fixed, the script will exit with code 0.

To run this script, save it to a file named `reproducer.py` in the root directory of your project, then execute it using `python3 reproducer.py`.