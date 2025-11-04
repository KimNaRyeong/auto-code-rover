Here is the reproducer script:

```python
import urllib.request
from io import BytesIO
from contextlib import redirect_stdout
from tempfile import TemporaryFileDescriptor

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
    url = "https://bpaste.net"
    data = BytesIO()
    with redirect_stdout(data):
        from urllib.request import urlopen
        with open("data.txt", "rb") as in_fh:
            data.write(in_fh.read())
    data.seek(0)
    try:
        response = urllib.request.urlopen(url, data=data.getvalue(), headers={'Content-Type': 'text/plain'})
        if response.getcode() != 200:
            raise AssertionError(f"Expected HTTP 200, got {response.getcode()}")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script attempts to reproduce the issue by sending a POST request to `bpaste.net` with the contents of `data.txt`. If the response status code is not 200, it raises an `AssertionError`, which will be caught and printed along with its stack trace.