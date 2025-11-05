Here is the reproducer script:

```python
import xarray as xr
import pandas as pd
from functools import wraps

def assert_raises(expected_exception):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except expected_exception as e:
                print_stacktrace(e)
                raise AssertionError("Expected exception not raised")
            else:
                raise AssertionError("Expected exception not raised")
        return wrapper
    return decorator

@assert_raises(NotImplementedError)
def reproducer():
    da = xr.DataArray([[[1]]], dims=["a", "b", "c"]).stack(ab=["a", "b"])
    try:
        da.to_series()
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproducer()
```

This script will reproduce the issue by calling `da.to_series()` and catch any exceptions that are raised. If an exception is caught, it will print a stack trace using the provided function and raise an assertion error if the expected exception (`NotImplementedError`) was not raised.