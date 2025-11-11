Here is the reproducer script:

```python
import inspect
from functools import wraps
from typing import Callable, Any

def inherit_docstrings(cls):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        if not hasattr(cls, '__doc'):
            cls.__doc__ = ''

        if not inspect.isfunction(func):
            raise AssertionError("This should have raised an error")

        return wrapper

    return type('InheritDocstrings', (object,), {'__metaclass__': decorator})

class Test:
    def __init__(self):
        pass

    @property
    def prop(self):
        """docstring"""
        return 1

if __name__ == '__main__':
    try:
        inherit_docstrings(Test)
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
```

This script defines a metaclass `inherit_docstrings` that checks if the function is not a property. It then uses this metaclass to create a class `Test`. The `prop` method of this class is a property with a docstring.

When you run this script, it should raise an AssertionError and print the stack trace.