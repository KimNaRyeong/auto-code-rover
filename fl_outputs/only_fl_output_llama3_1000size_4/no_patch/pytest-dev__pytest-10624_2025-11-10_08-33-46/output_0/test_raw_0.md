Here is the reproducer script:

```python
import pytest
import sys
from _pytest.python_api import approx

def test_foo_dict():
    a = {'foo': 42.0}
    b = {'foo': 0.0}
    assert a == approx(b)

if __name__ == "__main__":
    try:
        test_foo_dict()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script will raise an `AssertionError` when the issue is present and print the stack trace. If you run this script, it should reproduce the original issue.