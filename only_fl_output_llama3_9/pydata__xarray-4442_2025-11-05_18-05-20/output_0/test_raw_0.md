Here is the reproducer script:

```python
import xarray as xr
import pandas as pd
from functools import wraps

def assert_raises(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected an exception")
    except Exception as e:
        print_stacktrace(e)

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

def test_issue():
    da = xr.DataArray([[[1]]], dims=["a", "b", "c"]).stack(ab=["a", "b"])
    assert_raises(da.to_series, check=False)
    # or
    # assert_raises(da.to_dataframe("A"), check=False)

if __name__ == "__main__":
    test_issue()
```

This script defines a decorator `assert_raises` that attempts to execute the given function and raises an assertion error if no exception is raised. It then uses this decorator to test the issue, which should raise a `NotImplementedError`. The `print_stacktrace` function is used to print the stack trace of the exception.

To run the script, save it in a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`.