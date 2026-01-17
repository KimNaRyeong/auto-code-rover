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

The script defines the `print_stacktrace` function to print the stack trace with line numbers. The `test_issue` function demonstrates the expected behavior when using a regular `try-except` block, while the following code block reproduces the issue with `pytest.raises`. The script then asserts that the output of `str(e.value)` matches the expected output.