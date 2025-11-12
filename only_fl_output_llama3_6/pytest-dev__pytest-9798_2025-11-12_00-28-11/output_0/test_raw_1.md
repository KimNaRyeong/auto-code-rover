Here is the reproducer script:

```python
import pytest
from _pytest.python_api import approx

def test_approx():
    try:
        assert [1, 2] == pytest.approx([1.001, 2.002])
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

try:
    test_approx()
except SystemExit as e:
    if e.code != 0:
        raise
    exit(0)
```

This script can be run with `python3 reproducer.py` and should reproduce the issue.