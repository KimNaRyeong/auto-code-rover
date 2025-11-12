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
    from _pytest.python_api import approx
except ImportError:
    print("Error: pytest not installed")
    exit(0)

test_approx()
```

This script should reproduce the issue by raising an `AssertionError` when run with `python3 reproducer.py`.