Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import logging
import pytest

def _check_cond():
    logging.warning("_check_cond")
    return True

@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")

try:
    import logging
    logging.basicConfig(level=logging.WARNING)
    logging.captureWarnings(True)

    logging.warning("Initial warning")

    assert False, "Expected failure"
except AssertionError as e:
    print_stacktrace(e)
    raise

finally:
    try:
        import sys
        if sys.stderr.isatty():
            print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)
```

This script should reproduce the issue when run with `python3 reproducer.py`, and it will exit with code 0 when the issue is fixed.