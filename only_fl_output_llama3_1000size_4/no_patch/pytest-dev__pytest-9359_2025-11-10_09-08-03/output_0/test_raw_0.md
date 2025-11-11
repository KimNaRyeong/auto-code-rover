Here is the reproducer script:

```python
from functools import wraps
from pytest import fixture

def t(foo):
    return foo

@fixture
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

    assert 2 == outer

try:
    test_right_statement(None)
except AssertionError as e:
    print_stacktrace(e)
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.