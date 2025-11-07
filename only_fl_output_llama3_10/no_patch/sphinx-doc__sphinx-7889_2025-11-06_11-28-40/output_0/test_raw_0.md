Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import typing as t
from sphinx.ext import autodoc

def reproduce_issue():
    class GenericClass(t.Generic):
        T: t.TypeVar('T')

        def __init__(self, value: t.TypeVar('T')):
            pass

    @autodoc.mock
    class MockGenericClass(GenericClass[int]):
        pass

    try:
        autodoc.mock._make_subclass(MockGenericClass)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script defines a generic class `GenericClass` with a type variable `T`, and then creates a mock class `MockGenericClass` that inherits from `GenericClass[int]`. The script then attempts to create an instance of the mock class using `autodoc.mock._make_subclass`, which should raise a TypeError due to the concatenation of a `str` to a `TypeVar`.

When you run this script with Python 3.7.7, it should print the stack trace and raise an AssertionError indicating that the issue has been reproduced.

Note: You may need to modify the script to match your specific project setup and environment.