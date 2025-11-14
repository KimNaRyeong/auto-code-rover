Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
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

try:
    test_right_statement(1)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This file should be executed by running `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace with the line numbers.