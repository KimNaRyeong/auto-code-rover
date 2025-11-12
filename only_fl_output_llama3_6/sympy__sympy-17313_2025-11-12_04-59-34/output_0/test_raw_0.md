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

def test():
    assert math.ceil(-1) <= 0
    assert math.floor(-1) < 0
    assert math.floor(1) >= 0
    assert math.ceil(1) > 0

try:
    test()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Test passed")
    exit(0)
```

This script defines a `test` function that calls the `math.ceil` and `math.floor` functions with different arguments, and asserts that the results are correct. If any of these assertions fail, it catches the `AssertionError`, prints the stack trace using the provided `print_stacktrace` function, and exits with code 1. If all assertions pass, it prints a success message and exits with code 0.