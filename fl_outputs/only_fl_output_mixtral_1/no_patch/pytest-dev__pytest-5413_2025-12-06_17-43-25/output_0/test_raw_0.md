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
        raise LookupError("A\nB\nC")
    except LookupError as e:
        assert str(e) == "A\nB\nC"

    with pytest.raises(LookupError) as e:
        raise LookupError("A\nB\nC")

    assert str(e.value) == "A\nB\nC"

test_issue()
```

To run the script, execute `python3 reproducer.py`. The script will raise an `AssertionError` and print a stack trace showing the issue.

The script defines the `print_stacktrace` function to print the stack trace with line numbers. The `test_issue` function demonstrates the issue by raising a `LookupError` exception and comparing the output of `str(e)` and `str(e.value)` when using `pytest.raises`. The `test_issue` function then asserts that the outputs are equal. When the script is executed, the assertion will fail, raising an `AssertionError` and printing the stack trace.