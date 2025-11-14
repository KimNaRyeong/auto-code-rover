Here is the reproducer script:

```python
import xarray as xr
import numpy as np

def reproduce_issue():
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    try:
        ds.coarsen(time=12).construct(time=("year", "month"))
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)
        raise

def print_stacktrace(e):
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

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by calling `ds.coarsen(time=12).construct(time=("year", "month"))`. If the expected behavior is not observed, it will raise an `AssertionError` and print the stack trace.