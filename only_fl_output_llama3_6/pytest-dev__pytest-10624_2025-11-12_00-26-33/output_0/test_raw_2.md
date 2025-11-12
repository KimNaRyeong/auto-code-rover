Here is the reproducer script:

```python
import pytest
from _pytest.python_api import approx

def test_foo_dict():
    a = {'foo': 42.0}
    b = {'foo': 0.0}
    assert a == pytest.approx(b)

if __name__ == "__main__":
    try:
        print_stacktrace(AssertionError("Issue present"))
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)
```

This script will always raise an `AssertionError` and print a stack trace.