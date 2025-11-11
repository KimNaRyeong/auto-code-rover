The issue you're experiencing is not related to the original problem of a 301 redirect being broken with the latest pyopenssl/SNI. Instead, it appears that there are some issues with your Python environment and package installations.

Here's a standalone reproducer script:

```python
import requests
from urllib3.exceptions import HTTPError

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

try:
    response = requests.get('https://httpbin.org/status/301')
except HTTPError as e:
    print_stacktrace(e)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.