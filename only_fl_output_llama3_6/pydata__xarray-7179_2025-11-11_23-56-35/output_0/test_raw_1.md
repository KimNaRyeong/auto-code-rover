Here is the reproducer script:

```python
import time
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
        import xarray
        if time.time() - 1.5 < end_time:
            raise AssertionError("Importing xarray took too long")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

reproduce_issue()
```

This script uses a timing decorator to measure the time it takes for the `reproduce_issue` function to execute. The function attempts to import the `xarray` package and checks if the execution took more than 1.5 seconds. If so, it raises an `AssertionError` with a stack trace.

Please note that this script will exit with code 1 when the issue is present (i.e., importing xarray takes too long).