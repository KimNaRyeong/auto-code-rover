Here is the reproducer script:

```python
import django
from django.forms import DurationField
from django.utils.dateparse import parse_duration
from functools import wraps

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

def reproduce_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")
    return wrapper

@reproduce_issue
def test_duration_field():
    duration_field = DurationField()
    duration_field.clean('P3(3D')

if __name__ == "__main__":
    try:
        test_duration_field()
    except AssertionError as e:
        print(f"AssertionError: {e}")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise
```

This script sets up a `DurationField` and attempts to clean the input string `'P3(3D'`. If an exception is raised, it prints the stack trace using the provided function and raises an `AssertionError` to indicate that the issue was reproduced.