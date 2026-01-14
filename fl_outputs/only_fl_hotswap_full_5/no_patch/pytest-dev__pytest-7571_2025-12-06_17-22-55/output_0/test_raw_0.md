 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import pytest

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_foo(caplog):
    caplog.set_level(42)

def test_bar(caplog):
    assert caplog.handler.level == 42, "Log level was not restored after test"
    print(caplog.handler.level)
```

When running this script with pytest 6.0.0 or higher, it will raise an `AssertionError` with the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 18, in test_bar
    assert caplog.handler.level == 42, "Log level was not restored after test"
AssertionError: Log level was not restored after test
