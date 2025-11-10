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
    import sys
    from io import StringIO
    original_stderr = sys.stderr
    captured_stderr = StringIO()
    sys.stderr = captured_stderr
    
    pytest.main(["-v", "-s", "test_logging.py"])
    
    sys.stderr = original_stderr
    
    assert "WARNING:root:Schmift" not in captured_stderr.getvalue(), "Expected logging message to be printed only once"
except AssertionError as e:
    print_stacktrace(e)
    raise
```

This script can be run using `python3 reproducer.py`. It should raise an `AssertionError` when the issue is present and print a stack trace of the issue.