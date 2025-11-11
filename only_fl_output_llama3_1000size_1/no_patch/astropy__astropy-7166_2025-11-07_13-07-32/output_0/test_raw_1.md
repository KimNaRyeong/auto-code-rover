Here is the reproducer script:

```python
def inherit_docstrings(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__doc__ = func.__doc__
        return wrapper
    return type('InheritDocstrings', (cls,), {'__call__': decorator})

class Test:
    def __init__(self):
        pass

    @property
    def prop(self):
        """This is a property docstring"""
        return 1

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

if __name__ == "__main__":
    try:
        class TestDocstring:
            def __init__(self):
                pass

            @property
            def prop(self):
                """This is a property docstring"""
                return 1

        inherit_docstrings(type)(TestDocstring())
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

To run the script, execute `python3 reproducer.py` in your terminal. This should raise an exception and print a stack trace showing the line numbers of the statements.