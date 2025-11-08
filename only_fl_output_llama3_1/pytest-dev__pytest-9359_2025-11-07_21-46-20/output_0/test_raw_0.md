Here is the reproducer script:

```python
from functools import wraps
import pytest

def t(foo):
    return foo

@pytest.fixture
def foo():
    return 1

def test_right_statement(foo):
    assert foo == (3 + 2) * (6 + 9)

    @t
    def inner():
        return 2

    assert 2 == inner

    @t
    def outer():
        return 2

    print_stacktrace(AssertionError("1 != 75"))

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

This script should be run with `python3 reproducer.py` and it will raise an `AssertionError` when the issue is present.