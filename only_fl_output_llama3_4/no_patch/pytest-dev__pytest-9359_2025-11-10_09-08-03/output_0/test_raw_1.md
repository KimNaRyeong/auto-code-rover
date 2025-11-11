Here is the reproducer script:

```python
def t(foo):
    return foo

@t
def outer():
    return 2

def test_right_statement():
    assert 1 == (3 + 2) * (6 + 9)

try:
    test_right_statement()
except AssertionError as e:
    print_stacktrace(e)
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.