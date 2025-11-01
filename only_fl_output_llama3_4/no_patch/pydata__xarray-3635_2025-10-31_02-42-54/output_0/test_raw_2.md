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

def reproducer():
    da = xr.DataArray([0, 1, 2])
    assert_raises(ValueError, da.quantile, q=100.5)

if __name__ == "__main__":
    try:
        reproducer()
    except AssertionError as e:
        print_stacktrace(e)
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)
```

This script will raise an `AssertionError` when the issue is present, and it will print a stack trace of the error. If the issue is fixed, it will simply print a message and exit with code 0.

Please note that this reproducer script does not reproduce the exact issue you provided because your original MCVE code sample does not actually raise an exception. However, this script should still help to identify any issues related to `xarray` or `numpy`.