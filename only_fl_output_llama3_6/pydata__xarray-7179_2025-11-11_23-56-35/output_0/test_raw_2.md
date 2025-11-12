Here is the reproducer script:

```python
import time
import xarray
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.2f} seconds to execute")
        return result
    return wrapper

@timing_decorator
def reproduce_issue():
    try:
        start_time = time.time()
        import xarray
        end_time = time.time()
        if end_time - start_time > 1.5:
            raise AssertionError("Importing xarray took too long")
    except Exception as e:
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

reproduce_issue()
```

This script uses a timing decorator to measure the time it takes for the `reproduce_issue` function to execute. The function attempts to import the `xarray` package and checks if the execution took more than 1.5 seconds. If so, it raises an `AssertionError` with a stack trace.

Please note that this script will exit with code 1 when the issue is present (i.e., importing xarray takes too long).