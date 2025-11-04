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
    year = 2022
    expected_result = "0022"
    actual_result = dateformat.DateFormat(year).Y()
    assert actual_result == expected_result, f"Expected '{expected_result}' but got '{actual_result}'"

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```

This script will run the reproducer function when executed with `python3 reproducer.py`. The reproducer function tries to format a date using the "Y" specifier and checks if the result is equal to the expected result. If the assertion fails, it prints the stack trace and raises the exception again.