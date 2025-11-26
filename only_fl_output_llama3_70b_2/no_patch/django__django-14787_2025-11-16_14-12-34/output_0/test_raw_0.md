Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import functools
import logging

def wraps(func):
    def decorator(wrapper):
        wrapper.__name__ = func.__name__
        wrapper.__module__ = func.__module__
        return wrapper
    return decorator

def method_decorator(decorator):
    def decorator_wrapper(func):
        partial_func = functools.partial(func.__func__, func.__self__)
        return decorator(partial_func)
    return decorator_wrapper

def logger(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = str(e)
        finally:
            logging.debug(f"{func.__name__} called with args: {args} and kwargs: {kwargs} resulting: {result}")
    return inner

class Test:
    @method_decorator(logger)
    def hello_world(self):
        return "hello"

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

logging.basicConfig(level=logging.DEBUG)

try:
    test = Test()
    test.hello_world()  # This should raise an AttributeError
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected AttributeError due to missing __name__ attribute"
```
This script defines the `method_decorator` and `logger` decorators, and a `Test` class with a decorated method `hello_world`. When run, it should raise an `AttributeError` due to the missing `__name__` attribute on the partial object. The `print_stacktrace` function is used to print the stack trace of the exception.

If the issue is fixed, the script will exit with code 0. If the issue is present, the script will raise an `AssertionError`.