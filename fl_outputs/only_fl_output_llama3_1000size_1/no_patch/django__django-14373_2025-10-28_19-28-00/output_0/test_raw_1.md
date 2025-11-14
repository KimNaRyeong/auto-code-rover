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
        date = django.utils.datetime_safe.datetime(123, 1, 1)
        date_str = dateformat.format(date, 'Y')
        assert len(date_str) == 4 and date_str[0] != '0', "DateFormat.Y() is not zero-padded"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to format a datetime object with the year `123` using the `'Y'` format specifier from Django's dateformat module. If the resulting string is not four characters long and does not start with a zero, it will raise an AssertionError with a message indicating that the issue is present. The `print_stacktrace` function is used to print the stack trace of the exception.