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
    pytest.main(["test_logging.py"])
except SystemExit as e:
    if e.code != 0:
        print_stacktrace(e)
        raise
```

This script will run the `test_logging` function with the `@pytest.mark.skipif` marker, which should cause the logging calls to be duplicated to stderr. The script also includes a try-except block to catch any exceptions that may occur during the test execution and prints the stack trace if an assertion error occurs.