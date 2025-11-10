I apologize for the previous mistake. Here is a new reproducer script that should reproduce the issue:

```python
def inherit_docstrings(cls):
    def decorator(func):
        if not hasattr(cls, '__doc'):
            cls.__doc__ = ''

        if not inspect.isfunction(func) and not isinstance(func, property):
            raise AssertionError("This should have raised an error")

        return func

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
        class Test2:
            __doc__ = 'Test docstring'
            @inherit_docstrings
            @property
            def prop(self):
                """docstring"""
                return 1
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

```

This script defines a metaclass `inherit_docstrings` that checks if the function is not a property. It then uses this metaclass to create a class `Test2`. The `prop` method of this class is a property with a docstring.

When you run this script, it should raise an AssertionError and print the stack trace.