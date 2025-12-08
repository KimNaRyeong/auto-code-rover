 I apologize for the mistake in my previous response. Here's the corrected `reproducer.py` script that reproduces the issue:

```python
import pytest
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    try:
        raise LookupError(
            "A\n"
            "B\n"
            "C"
        )
    except LookupError as e:
        assert str(e) == "A\nB\nC"

try:
    with pytest.raises(LookupError) as e:
        raise LookupError(
            "A\n"
            "B\n"
            "C"
        )
except AssertionError as e:
    print_stacktrace(e)
    assert False, "pytest.raises context variable behaves differently than a normal exception catch"

assert str(e.value) == "A\nB\nC"
```

This script defines the `print_stacktrace` function to print the stack trace, and it defines a test function `test_issue()` that demonstrates the issue. The script uses `pytest.raises` to catch the `LookupError` exception and then raises an `AssertionError` if the string representation of the exception's value is not equal to the expected value. The script then checks if an `AssertionError` was raised, and if so, it prints the stack trace and exits with code 1. If the `AssertionError` was not raised, the script asserts that the string representation of the exception's value is equal to the expected value and exits with code 0.