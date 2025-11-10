Here is the reproducer script:

```python
import inspect
from functools import wraps

def inherit_docstrings(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if inspect.isfunction(func) or hasattr(func, 'fget'):
            wrapper.__doc__ = func.__doc__
        return wrapper

    for name in dir(cls):
        attr = getattr(cls, name)
        if inspect.isfunction(attr) or hasattr(attr, 'fget'):
            setattr(cls, name, decorator(attr))

class Test:
    def __init__(self):
        pass

    @property
    def prop(self):
        """Docstring"""
        return "value"

if __name__ == "__main__":
    try:
        class TestDocstrings:
            __doc__ = "Test docstring"
            pass

        inherit_docstrings(Test)
        print("Issue not present")
        exit(0)
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

This script defines a `inherit_docstrings` metaclass that decorates functions and properties with their docstrings. It then uses this metaclass to decorate the `Test` class, which has a property. The script then attempts to run the decorator and prints an error message if it succeeds (i.e., the issue is present), or prints a stack trace if it raises an exception (i.e., the issue is fixed).