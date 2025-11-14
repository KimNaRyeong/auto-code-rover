Here is the reproducer script:

```python
import pytest
from _pytest.python_api import approx

def test_approx():
    assert [1, 2] == approx([1.001, 2.002])

if __name__ == "__main__":
    try:
        test_approx()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed")
        exit(0)

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
```

This script will run the test function `test_approx` and catch any `AssertionError` that is raised. If an error is caught, it will print the stack trace using the provided `print_stacktrace` function and exit with code 1. If no error is caught, it will print "Test passed" and exit with code 0.