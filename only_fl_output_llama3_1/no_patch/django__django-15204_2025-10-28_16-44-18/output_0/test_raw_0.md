Here is the reproducer script:

```python
import django
from django.forms import DurationField
from django.utils.dateparse import parse_duration

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
    duration_field = DurationField()
    try:
        duration_field.clean('P3(3D')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    django.setup()  # Initialize Django
    reproduce_issue()
```

This script sets up a `DurationField` and attempts to clean the input string `'P3(3D'`. If an exception is raised, it prints the stack trace using the provided function and raises an `AssertionError` to indicate that the issue was reproduced.