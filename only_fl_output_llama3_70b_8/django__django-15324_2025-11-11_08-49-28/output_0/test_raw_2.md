Here is a standalone Python script `reproducer.py` to reproduce the issue:
```
import io
import requests
from urllib.parse import urlparse

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
    url = 'http://localhost:8000/'
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt\x00", contents, "text/plain")}
    
    try:
        req = requests.Request("POST", url, files=files)
        prepared = req.prepare()
        body = prepared.body
        assert isinstance(body, bytes)
        prepared.body = body.replace(b"!", b"\x00")
        response = requests.Session().send(prepared)
        if response.status_code == 500:
            raise AssertionError("Issue is present.")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```
This script sends a POST request to `http://localhost:8000/` with a file that has a null byte in its filename. If the issue is present, it should raise an `AssertionError` with a stack trace of the error.

Please note that you need to have a Django server running at `http://localhost:8000/` for this script to work.