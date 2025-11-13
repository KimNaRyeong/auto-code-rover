Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
import io
import requests
from django.http import HttpResponseServerError
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

def main():
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
    req = requests.Request("POST", "http://localhost:8000/", files=files)
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\x00")
    
    try:
        response = requests.Session().send(prepared)
        if response.status_code == 500:
            raise AssertionError("File upload crashed with a 500 error")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script sends a POST request to `http://localhost:8000/` with a file that has a null character in its filename. If the server returns a 500 error, it raises an `AssertionError`. If any other exception occurs during the request, it prints the stack trace using the provided function and exits with code 1.

To use this script, save it to a file named `reproducer.py` in the root directory of your project, then run it with `python3 reproducer.py`.