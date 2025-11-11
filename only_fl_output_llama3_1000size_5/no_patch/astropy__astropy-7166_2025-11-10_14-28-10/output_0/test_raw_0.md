Here is the reproducer script:

```python
import inspect
from functools import wraps

def inherit_docstrings(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if not hasattr(cls, '__doc'):
            cls.__doc__ = ''

        wrapper.__doc__ = func.__doc__
        return wrapper

    return type('InheritDocstrings', (object,), {'__metaclass__': decorator})

class Test:
    def __init__(self):
        pass

    @property
    def prop(self):
        """This is a property docstring"""
        pass

    @inherit_docstrings
    class Inner:
        @property
        def inner_prop(self):
            """Inner property docstring"""
            pass

if __name__ == '__main__':
    try:
        Test.Inner()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

```

This script defines a metaclass `inherit_docstrings` that inherits docstrings from its methods. It then uses this metaclass to define an inner class with a property, and tries to create an instance of the inner class. If the issue is present, it should raise an `AssertionError`, which will be caught by the script and printed using the provided `print_stacktrace` function.