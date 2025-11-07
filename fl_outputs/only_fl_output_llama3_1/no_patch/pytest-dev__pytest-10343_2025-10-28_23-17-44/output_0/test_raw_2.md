Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import pytest

def pytest_configure(config):
    pass  # This is the old-style hookimpl warning

print_stacktrace(None)

try:
    from plugin import *
except ImportError as e:
    print_stacktrace(e)
    assert False, "Expected pytest_deprecation_warning"

```

This script should raise an AssertionError and print a stack trace when run with `python3 reproducer.py`.