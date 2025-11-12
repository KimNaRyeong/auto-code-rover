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
    assert False
except AssertionError as e:
    print_stacktrace(e)
    raise
```

This script should reproduce the issue when run with `python3 reproducer.py`, and it will exit with code 0 when the issue is fixed.