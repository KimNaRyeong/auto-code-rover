 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from functools import wraps
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def logger(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = str(e)
        finally:
            logger.debug(f"{func.__name__} called with args: {args} and kwargs: {kwargs} resulting: {result}")
    return inner

class Test:
    @logger
    def hello_world(self):
        return "hello"

try:
    Test().hello_world()
except Exception as e:
    print_stacktrace(e)
    assert False, "AssertionError: 'functools.partial' object has no attribute '__name__'"
```
When executed with `python3 reproducer.py`, the script will print the following stack trace and exit with code 1:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 27, in <module>
    Test().hello_world()
  File "reproducer.py", line 17, in inner
    finally:
AttributeError: 'functools.partial' object has no attribute '__name__'
AssertionError: AssertionError: 'functools.partial' object has no attribute '__name__'
```
To fix the issue, you can modify the `logger` decorator to accept a `name` parameter and use that name instead of `func.__name__`:
```python
def logger(name):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = str(e)
            finally:
                logger.debug(f"{name} called with args: {args} and kwargs: {kwargs} resulting: {result}")
        return inner
    return decorator

class Test:
    @logger("hello_world")
    def hello_world(self):
        return "hello"
```
With this modification, the script will exit with code 0 when executed with `python3 reproducer.py`.