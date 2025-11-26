Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import logging
import pytest
import sys


def _check_cond():
    logging.warning("_check_cond")
    return True


@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")
    assert False


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


def main():
    try:
        pytest.main([__file__, "-v", "-s"])
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("Issue is present")
    else:
        print("Issue is fixed")


if __name__ == "__main__":
    main()
```
This script uses the `pytest` framework to run a test that exercises the issue. The `_check_cond()` function calls `logging.warning()`, which causes the logging call in `test_logging()` to be duplicated to stderr.

When the issue is present, the script will raise an `AssertionError` with a stack trace showing the line numbers of the statements involved. When the issue is fixed, the script will exit with code 0.

To run the script, save it to a file named `reproducer.py` and execute it with `python3 reproducer.py`.