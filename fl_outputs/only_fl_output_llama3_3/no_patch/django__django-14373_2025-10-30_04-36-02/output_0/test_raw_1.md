Here is the reproducer script:

```python
import django
from django.utils import dateformat

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
        year = 123
        date_obj = django.utils.datetime_safe.datetime(1, 1, year)
        formatted_date = dateformat.format(date_obj, 'Y')
        assert len(str(formatted_date)) == 4, "Expected a four-digit year"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the reproducer function when executed with `python3 reproducer.py`. If the issue is present, it will print the stack trace and raise an `AssertionError`.