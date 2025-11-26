Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
import pytest

def test_not_found_by_ini(testdir):
    testdir.makeini("""
        [pytest]
        addopts = -k
    """)
    testdir.makepyfile("""
        def test_not_found():
            pass
    """)
    result = testdir.runpytest("-k", "test_not_found_by_ini")
    try:
        result.assert_outcomes(passed=2)
    except AssertionError as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    test_not_found_by_ini(pytest.config.Testdir("path/to/test"))
```
This script creates a temporary pytest configuration and runs a test that should pass. It then tries to assert the outcome of the test using `assert_outcomes(passed=2)`. If the assertion fails due to the presence of the `deselected` parameter, it prints the stack trace of the error and raises an `AssertionError`.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.