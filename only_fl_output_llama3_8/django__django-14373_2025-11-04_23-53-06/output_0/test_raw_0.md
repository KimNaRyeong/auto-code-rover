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
    year = 500
    formatted_date = dateformat.format(year, 'Y')
    assert len(formatted_date) == 4, f"Expected a four-digit year, but got {formatted_date}"
    print_stacktrace(AssertionError())

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the reproducer function when executed with `python3 reproducer.py`. The reproducer function formats a date using the 'Y' specifier and checks if the result is a four-digit year. If not, it raises an `AssertionError` which will be caught by the `print_stacktrace` function to print the stack trace of the issue.