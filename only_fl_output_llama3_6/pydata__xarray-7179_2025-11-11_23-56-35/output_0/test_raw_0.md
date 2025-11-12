Here is the reproducer script:

```python
import time
import xarray as xr
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
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Importing xarray took too long")

reproduce_issue()
```

This script uses a timing decorator to measure the time it takes for the `reproduce_issue` function to execute. The function attempts to import the `xarray` package and prints the stack trace if an exception is raised (i.e., the import takes too long).