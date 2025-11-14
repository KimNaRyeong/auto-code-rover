Here is the reproducer script:

```python
import sys
from functools import wraps

def wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e.__cause__
    return wrapper

@wrapper
def test():
    exc = WrapperException("Test exception")
    raise exc

class WrapperException(Exception):
    pass

if __name__ == "__main__":
    try:
        test()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

```

This script defines a `WrapperException` class and a `test()` function that raises an instance of this exception. The `wrapper()` decorator is used to catch the exception and re-raise its cause.