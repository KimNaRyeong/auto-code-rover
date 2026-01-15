```python
import pytest
import sys


def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def test_foo(caplog):
    caplog.set_level(42)


def test_bar(caplog):
    assert caplog.handler.level == 0, "caplog handler level was not restored after test"


if __name__ == "__main__":
    try:
        # Dynamically creates a test suite, this ensures our test runner remains generic and relies on pytest's discovery mechanism.
        pytest_args = ['reproducer.py', '-vv']

        # Run pytest with our tests and capture the output
        result = pytest.main(pytest_args)

        # Check if pytest encountered any errors (exit code 0 means all tests passed)
        if result != 0:
            raise AssertionError("Pytest did not exit cleanly. This could indicate a failure in the functionality being tested.")

    except AssertionError as ae:
        print_stacktrace(ae)
        sys.exit(1)

    print("Test completed successfully, the issue is fixed.")
    sys.exit(0)
```