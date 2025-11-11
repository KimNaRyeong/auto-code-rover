Here is the reproducer script:

```python
from functools import wraps

def t(foo):
    return foo

@fixture
def foo():
    return 1

def test_right_statement(foo):
    @wraps(t)
    def inner():
        return 2

    assert 2 == inner()

    @wraps(t)
    def outer():
        return 2
    assert 2 == outer()

try:
    test_right_statement()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.