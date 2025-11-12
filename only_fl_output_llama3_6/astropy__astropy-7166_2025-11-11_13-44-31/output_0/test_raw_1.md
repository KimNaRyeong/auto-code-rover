Here is the reproducer script:

```python
def inherit_docstrings(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if not hasattr(cls, '__doc'):
            cls.__doc__ = ''

        if not inspect.isfunction(func):
            raise AssertionError("InheritDocstrings metaclass doesn't work for properties")

        wrapper.__doc__ = f"{cls.__name__}.{func.__name__} - {wrapper.__doc__}"
        return wrapper

    return type(cls.__name__, (object,), {'__metaclass__': decorator})

class Parent:
    def __init__(self):
        pass

    @property
    def prop(self):
        """Docstring for prop"""
        pass

class Child(Parent, metaclass=inherit_docstrings):
    """Docstring for Child"""

try:
    child = Child()
    print(child.prop.__doc__)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present")
exit(0)
```

This script defines a `Parent` class with a property and a `Child` class that inherits from the `Parent` class. The `inherit_docstrings` metaclass is applied to the `Child` class, which checks if the decorated function is a function using `inspect.isfunction`. Since properties are not functions, this check will fail for the `prop` property in the `Parent` class.

When you run this script with Python 3.9 or earlier, it should raise an `AssertionError` and print the stack trace of the issue.