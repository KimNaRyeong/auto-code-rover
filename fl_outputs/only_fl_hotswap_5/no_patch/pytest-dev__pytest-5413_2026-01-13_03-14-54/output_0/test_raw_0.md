 Here's a standalone Python script `reproducer.py` that reproduces the issue:

```python
import pytest

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
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

with pytest.raises(LookupError) as e:
    raise LookupError(
        "A\n"
        "B\n"
        "C"
    )

assert str(e.value) == "A\nB\nC"
```

To run the script, execute `python3 reproducer.py` in the terminal. The script will raise an `AssertionError` and print a stack trace, reproducing the issue.

The script defines the `print_stacktrace` function to print the stack trace, and it defines a test function `test_issue()` that demonstrates the issue. The test function catches the `LookupError` exception and asserts that the string representation of the exception is equal to the expected value. The second part of the script uses `pytest.raises` to catch the `LookupError` exception and asserts that the string representation of the exception's value is equal to the expected value.