Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import logging
import pytest

def _check_cond():
    return True

@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")

try:
    import sys
    if __name__ == "__main__":
        pytest.main(["-v", "-s", "--capture=std", "test_logging.py"])
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)

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

This script will run the `test_logging` function with the `@pytest.mark.skipif` marker, which should cause the logging calls to be duplicated to stderr. The script also includes a try-except block to catch any assertions that may occur during the test execution and prints the stack trace if an assertion error occurs.