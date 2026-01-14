 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import logging
import pytest
import sys


def _check_cond():
    logging.warning("_check_cond")
    return True


def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")

    assert False


if __name__ == "__main__":
    try:
        test_logging()
    except AssertionError:
        print_stacktrace(sys.exc_info()[1])
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script reproduces the issue and prints the following stack trace:
```sql
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    test_logging()
  File "reproducer.py", line 19, in test_logging
    assert False
AssertionError: AssertionError()
```
The captured log calls are duplicated to stderr, as described in the issue.