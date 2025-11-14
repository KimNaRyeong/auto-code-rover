Here is a new reproducer script that should reproduce the issue:

```python
def inherit_docstrings(cls):
    def decorator(func):
        if not inspect.isfunction(func):
            raise AssertionError("This should be a function")
        return func

    return type('InheritDocstrings', (object,), {'__metaclass__': decorator})

class Test:
    @property
    def prop(self):
        """Property docstring"""
        pass

if __name__ == '__main__':
    try:
        inherit_docstrings(Test)
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

This script defines a metaclass `inherit_docstrings` that checks if the function is not a function using `inspect.isfunction`. It then tries to create an instance of this metaclass with the `Test` class, which has a property. If the issue is present, it should raise an `AssertionError`, which will be caught by the script and printed using the provided `print_stacktrace` function.