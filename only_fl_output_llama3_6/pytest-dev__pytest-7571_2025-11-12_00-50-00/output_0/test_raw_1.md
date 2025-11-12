Here is the reproducer script:

```python
import pytest
from functools import wraps

def test_foo(caplog):
    caplog.set_level(42)

def test_bar(caplog):
    assert caplog.handler.level == 0, "Expected log level to be restored"

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

if __name__ == "__main__":
    try:
        pytest.main(["-v", "-k", "test_"])
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("Test failed")
        else:
            print("Test passed")
```

This script will run the tests and check if they pass or fail. If the tests fail, it will raise an `AssertionError`.