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

    with pytest.raises(LookupError) as e_info:
        raise LookupError(
            "A\n"
            "B\n"
            "C"
        )

    assert str(e_info.value) == "A\nB\nC"

test_issue()
```

To run the script, execute `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised, and the stack trace will be printed. If the issue is fixed, the script will exit with code 0.