Here is the reproducer script:

```python
from functools import wraps
import inspect
import sys
import traceback

def inherit_docstrings(cls):
    metaclass = type(cls.__name__, (object,), {})
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if hasattr(attr, '__get__') or hasattr(attr, '__set__'):
            if inspect.isfunction(attr) or isinstance(attr, property):
                @wraps(attr)
                def wrapper(*args, **kwargs):
                    return attr(*args, **kwargs)

                if not inspect.isfunction(wrapper) and isinstance(wrapper, property):
                    wrapper.__doc__ = cls.__doc__
                else:
                    wrapper.__doc__ = attr.__doc__

                setattr(cls, attr_name, wrapper)
    return metaclass

class TestClass:
    def __init__(self):
        pass

    @property
    def test_property(self):
        """This is a test property"""
        pass


@inherit_docstrings(TestClass)
class InheritDocstringsMeta(type):
    pass


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