Here is the reproducer script:

```python
import requests
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch, Mock
import sys
import traceback
import os

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    s = requests.Session()
    response = s.get('http://server.example.com/do_something')
    response = s.resolve_redirects(response, max_forwards=10)
    with StringIO() as f:
        with redirect_stdout(f):
            try:
                s.request('POST', 'http://failover.example.com/new_thing_1513')
            except Exception as e:
                print_stacktrace(e)
                os._exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a `requests.Session()` and then simulates the given redirection chain. It then attempts to send a POST request to the final URL, which should raise an exception due to the incorrect method selection. The script prints the stack trace of the exception and exits with code 1.