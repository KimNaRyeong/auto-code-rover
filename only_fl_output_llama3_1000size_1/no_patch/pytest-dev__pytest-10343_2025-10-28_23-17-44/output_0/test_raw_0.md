Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import pytest
from _pytest.config import hooks

def pytest_configure(config):
    pass  # This is the old-style hookimpl warning

try:
    pytest.main([])
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected pytest_deprecation_warning"

```

You can run this script by executing `python3 reproducer.py`. If you have the correct version of pytest installed (which includes the deprecation warning), it should raise an AssertionError and print a stack trace.