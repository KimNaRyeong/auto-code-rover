Here is the reproducer script:

```python
import pytest
import sys
from _pytest.outcomes import Skipped

def test_0(bar):
    assert 0

@pytest.fixture
def bar():
    if True:
        pytest.skip("Skipping")

if __name__ == "__main__":
    try:
        pytest.main([__file__, "-rs"])
    except SystemExit as e:
        if e.code != 0:
            print_stacktrace(e)
        sys.exit(e.code)
```

This script defines a test function `test_0` that always fails, and a fixture `bar` that skips the test based on some condition. When you run this script with `python3 reproducer.py`, it should reproduce the issue by showing a summary of skipped tests without indicating which test was skipped.