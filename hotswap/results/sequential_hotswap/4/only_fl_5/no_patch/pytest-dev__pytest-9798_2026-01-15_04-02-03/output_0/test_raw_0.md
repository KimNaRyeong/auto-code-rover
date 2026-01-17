```python
# reproducer.py
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

def test_approx():
    import pytest
    try:
        assert [1, 2] == pytest.approx([1.001, 2.002])
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_approx()
    except Exception as e:
        print("Test failed with exception:", str(e))
        exit(1)
    print("Test succeeded, no issue observed.")
    exit(0)
```

This standalone Python script is designed to reproduce the described issue when executed with Python 3.9.0 and pytest 7.0.1, within the specified environment. It should raise an `AssertionError` due to the failing assertion in the `test_approx()` function, and if the issue described is present, it will also print out a stack trace that includes the `ModuleNotFoundError` for numpy when the `pytest.approx` comparison fails.