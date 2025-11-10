Here is the reproducer script in a code block:

```python
import django.utils.dateparse
from datetime import datetime

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
    try:
        django.utils.dateparse.parse_datetime("2012-04-23T10:20:30.400 -02")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected parse_datetime to not raise an error")

if __name__ == "__main__":
    reproduce_issue()
```

This script tries to parse the given ISO-8601 datetime string using Django's `parse_datetime` function. If the parsing fails and raises any exception, it prints the stack trace and raises an `AssertionError`.