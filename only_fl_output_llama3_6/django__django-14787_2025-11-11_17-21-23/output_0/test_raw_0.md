Here is the reproducer script:

```python
import functools
from logging import debug as logger
from unittest import TestCase

def method_decorator(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = str(e)
        finally:
            logger(f"{func.__name__} called with args: {args} and kwargs: {kwargs} resulting: {result}")
        return result
    return inner

class Test(TestCase):
    @method_decorator
    def test_method(self, *args, **kwargs):
        pass

if __name__ == "__main__":
    try:
        Test().test_method()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected AttributeError: 'functools.partial' object has no attribute '__name__'"
    else:
        print("Issue fixed")
        exit(0)

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

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.