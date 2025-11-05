Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from functools import wraps

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

def assert_raises(expected_exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected an exception but didn't get one")
    except expected_exception as e:
        print_stacktrace(e)
        exit(0)

@wraps(xr.DataArray.quantile)
def reproducer(q=50):
    da = xr.DataArray([0, 1, 2])
    da.quantile(q=q)

if __name__ == "__main__":
    assert_raises(ValueError, reproducer, q=100)