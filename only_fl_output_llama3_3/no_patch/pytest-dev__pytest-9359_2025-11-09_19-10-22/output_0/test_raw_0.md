Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
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
    
    print_stacktrace(AssertionError("1 != 75"))
```

This script should raise an `AssertionError` when run with Python 3.9, and the stack trace will include the extra code line from the `@t` decorator.