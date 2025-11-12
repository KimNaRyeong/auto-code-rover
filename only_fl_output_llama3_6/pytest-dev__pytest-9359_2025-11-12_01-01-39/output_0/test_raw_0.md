Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import pytest
from functools import wraps

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

    assert 2 == inner()

    @t
    def outer():
        return 2

    print_stacktrace(AssertionError("Test failed"))
    assert False

if __name__ == "__main__":
    pytest.main([__file__])
```

This script defines the same test function `test_right_statement` as in your original issue, and uses the `print_stacktrace` function to print a stack trace when an `AssertionError` is raised.