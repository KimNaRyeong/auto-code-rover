Here is the reproducer script:

```python
import xarray as xr
import pandas as pd
from functools import wraps

def assert_raises(expected_exception, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except expected_exception as e:
            print_stacktrace(e)
            raise AssertionError("Expected exception not raised")
    return wrapper

@assert_raises(NotImplementedError, da.to_series)
def reproduce_issue():
    da = xr.DataArray([[[1]]], dims=["a", "b", "c"]).stack(ab=["a", "b"])
    da.to_series()

if __name__ == "__main__":
    reproduce_issue()
```

This script defines a decorator `assert_raises` that checks if the function it's applied to raises the expected exception. If not, it prints the stack trace and raises an `AssertionError`. The `reproduce_issue` function is then decorated with this decorator and called at the end of the script.

When you run this script, it should print a stack trace and raise an `AssertionError`, indicating that the issue is present.