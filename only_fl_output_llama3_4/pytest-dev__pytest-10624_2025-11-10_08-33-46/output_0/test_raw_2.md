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
        test_foo_dict()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script should reproduce the original issue when run with `python3 reproducer.py`.