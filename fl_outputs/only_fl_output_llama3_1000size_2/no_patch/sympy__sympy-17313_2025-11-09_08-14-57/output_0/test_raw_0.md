Here is the reproducer script:

```python
import math

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

def test_ceiling_floor():
    assert math.ceil(-1) <= 0
    assert math.floor(-1) < 0
    assert math.ceil(1) > 0
    assert math.floor(1) >= 0

try:
    test_ceiling_floor()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed!")
exit(0)
```

This script defines a function `test_ceiling_floor` that tests the ceiling and floor functions with some sample inputs. It then calls this function and catches any `AssertionError` exceptions that are raised. If an exception is caught, it prints the stack trace using the provided `print_stacktrace` function and exits with code 1. Otherwise, it prints a success message and exits with code 0.