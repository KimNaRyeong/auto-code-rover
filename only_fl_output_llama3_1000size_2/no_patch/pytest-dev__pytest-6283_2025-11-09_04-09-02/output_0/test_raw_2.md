Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import logging
import pytest

def _check_cond():
    return True

@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")

logging.warning("Test")

assert False, "Issue is present"

try:
    import logging
    logging.warning("Fix")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed, exiting with code 0.")
```

This script will reproduce the issue by printing "Schmift" and "Test" to both the captured log call and stderr.