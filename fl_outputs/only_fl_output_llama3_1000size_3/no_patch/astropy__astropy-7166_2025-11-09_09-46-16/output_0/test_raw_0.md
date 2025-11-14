Here is the reproducer script:

```python
import inspect
from functools import wraps
from typing import PropertyType

def inherit_docstrings(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if not inspect.isfunction(func) and isinstance(func, type):
            wrapper.__doc__ = cls.__doc__
        else:
            wrapper.__doc__ = func.__doc__

        return wrapper

    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if hasattr(attr, 'fget') or hasattr(attr, 'fset'):
            setattr(cls, attr_name, decorator(attr))

    return cls


class TestClass:
    def __init__(self):
        pass

    @property
    def test_property(self):
        """This is a test property"""
        pass


@inherit_docstrings(TestClass)
class InheritDocstringsMeta(type):
    def __new__(meta, name, bases, namespace):
        for attr_name in dir(namespace):
            attr = getattr(namespace, attr_name)
            if inspect.isfunction(attr) or isinstance(attr, type):
                if hasattr(attr, '__doc__'):
                    attr.__doc__ = f"{attr.__name__} {attr.__doc__}"
        return super().__new__(meta, name, bases, namespace)


class TestClassWithProperty(TestClass, metaclass=InheritDocstringsMeta):
    pass


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


try:
    TestClassWithProperty()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
exit(0)
```

This script defines a metaclass `InheritDocstringsMeta` that inherits docstrings from its base class. It then uses this metaclass to create a subclass `TestClassWithProperty` of the original test class, which has a property. The script attempts to reproduce the issue by creating an instance of `TestClassWithProperty`. If the issue is present (i.e., the assertion error is raised), it prints the stack trace and exits with code 1. Otherwise, it prints a success message and exits with code 0.