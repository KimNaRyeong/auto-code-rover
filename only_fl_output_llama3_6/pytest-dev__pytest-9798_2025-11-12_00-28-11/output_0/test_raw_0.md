Here is the reproducer script:

```python
import pytest
from _pytest.python_api import approx

def test_approx():
    assert [1, 2] == approx([1.001, 2.002])

try:
    test_approx()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script can be run with `python3 reproducer.py` and should raise an `AssertionError` when the issue is present.