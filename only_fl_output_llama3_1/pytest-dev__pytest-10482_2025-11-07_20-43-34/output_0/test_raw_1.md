Here is the reproducer script:

```python
import pytest
from _pytest.outcomes import Skipped

def test_0():
    assert 0

@pytest.fixture
def bar():
    if True:
        pytest.skip("Skipping")

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
        pytest.main([__file__, "-rs"])
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("Issue present")
        sys.exit(e.code)
```

This script defines a test function `test_0` that always fails, and a fixture `bar` that skips the test based on some condition. When you run this script with `python3 reproducer.py`, it should reproduce the issue by showing a summary of skipped tests without indicating which test was skipped.