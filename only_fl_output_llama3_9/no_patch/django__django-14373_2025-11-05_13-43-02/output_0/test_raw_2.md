Here is the reproducer script:

```python
import django
from django.utils import dateformat
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
        dt = datetime(500, 1, 1)
        date_string = dateformat.format(dt, 'Y')
        assert len(date_string) == 4 and date_string[0] == '0', "Expected a four-digit year padded with zeros"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the reproducer function when executed. If the issue is present, it will print the stack trace and raise an `AssertionError`.