Here is the reproducer script:

```python
import urllib.request
import os
from urllib.error import HTTPError
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    url = "https://bpaste.net"
    data = open("data.txt", "rb").read()
    
    try:
        response = urllib.request.urlopen(url, data=data)
        response.getcode()  # Raise an exception for bad status codes
    except HTTPError as e:
        print_stacktrace(e)
        raise AssertionError("HTTP error occurred")

if __name__ == "__main__":
    main()
```

This script attempts to upload the contents of `data.txt` to `bpaste.net`. If the request results in an HTTP error (400: Bad Request), it prints a stack trace and raises an `AssertionError`.