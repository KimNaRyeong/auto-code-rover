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
        datetime_str = "2012-04-23T10:20:30.400 -02"
        if ' ' in datetime_str:
            django.utils.dateparse.parse_datetime(datetime_str)
        else:
            raise AssertionError("Expected parse_datetime to not parse the given ISO-8601 datetime string")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected parse_datetime to not raise an error")

if __name__ == "__main__":
    reproduce_issue()
```

This script tries to create a datetime string with whitespace characters between the time strings and timezone strings. If Django's `parse_datetime` function can correctly parse this datetime string, it raises an `AssertionError`.