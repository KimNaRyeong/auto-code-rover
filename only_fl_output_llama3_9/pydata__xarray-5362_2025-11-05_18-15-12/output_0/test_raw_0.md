Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from functools import wraps

def assert_raises(func, *args, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Expected an error")
    return wrapper

@assert_raises
def reproducer():
    ds = xr.tutorial.open_dataset("air_temperature")
    ds.weighted(xr.ones_like(ds["air"])).mean("dummy")

if __name__ == "__main__":
    try:
        reproducer()
        print("Issue not present, exiting with code 0.")
        exit(0)
    except AssertionError as e:
        print(f"Issue present: {e}")
        exit(1)

```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.