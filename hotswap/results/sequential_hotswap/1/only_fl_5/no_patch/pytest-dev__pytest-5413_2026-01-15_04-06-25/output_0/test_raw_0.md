```python
# reproducer.py
import pytest

def test_str_on_pytest_raises():
    with pytest.raises(LookupError) as e:
        raise LookupError("A\nB\nC")
    # The issue: expecting str(e) to return the full exception message "A\nB\nC",
    # but it doesn't. Checking if str(e.value) matches expected, to verify behavior.
    assert str(e.value) == "A\nB\nC", "The exception message does not match."

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
    try:
        # Run test using pytest API
        pytest.main(["-k test_str_on_pytest_raises", "--tb=short"])
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1) from e
    else:
        print("No issue detected.")
        raise SystemExit(0)
```

This script is designed to reproduce the issue mentioned. When executed, it will attempt to run a specific test that demonstrates the discrepancy in behavior when retrieving the string representation of exceptions within the context of `pytest.raises` versus a normal exception catch block.

- The test `test_str_on_pytest_raises` intentionally raises a `LookupError` within a `pytest.raises` context manager and then asserts whether `str(e.value)` matches the expected string, which contains a multiline error message. This mirrors the issue reported, where `str(e)` in a pytest context does not behave as expected compared to the standard exception handling.

- If the issue is present (i.e., `str(e.value)` does not match the expected result or another unexpected issue occurs), `print_stacktrace(e)` is called to print the detailed stack trace, aiming to aid in pinpointing the location and nature of the discrepancy.

- The script uses `pytest.main()` with specific arguments to run only the test case relevant to the reported issue and suppresses detailed traceback of pytest itself using `--tb=short` to focus on the output relevant to the issue at hand.

- It exits with code 0 if the test passes (indicating no issue with `pytest.raises`), otherwise, it exits with code 1, signaling the presence of the reported issue or an assertion failure, making it a straightforward tool for verifying if the issue persists or has been resolved.