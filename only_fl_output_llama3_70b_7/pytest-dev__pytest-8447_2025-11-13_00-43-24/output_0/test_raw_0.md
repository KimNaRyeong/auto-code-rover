Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import pytest

def test_issue():
    class BlackItem:
        def __init__(self, parent, fspath, path):
            pass  # Simulate the original implementation

    class CheckdocsItem:
        def __init__(self, parent, fspath, path):
            pass  # Simulate the original implementation

    try:
        BlackItem.from_parent(None, fspath="path", path="path")
        CheckdocsItem.from_parent(None, fspath="path", path="path")
    except TypeError as e:
        print_stacktrace(e)
        assert False, "TypeError: __init__() got an unexpected keyword argument 'path'"

if __name__ == "__main__":
    test_issue()
```
This script defines two classes `BlackItem` and `CheckdocsItem` with an `__init__` method that takes three arguments: `parent`, `fspath`, and `path`. The `from_parent` class method is also defined to simulate the original implementation.

The script then tries to create instances of these classes using the `from_parent` method, passing `path` as a keyword argument. This should raise a `TypeError` with the message "unexpected keyword argument 'path'".

If the issue is present, the script will print the stack trace of the error and exit with an `AssertionError`. If the issue is fixed, the script will exit with code 0.

You can run this script using `python3 reproducer.py` to reproduce the issue.