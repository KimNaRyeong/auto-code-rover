Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import numpy as np

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

try:
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    coarsened_ds = ds.coarsen(time=12).construct(time=("year", "month"))

    assert all(coord.name not in ["day"] for coord in coarsened_ds.coords.values()), \
        f"Non-dimensional coordinates 'day' was demoted to a variable"

    print("Issue is fixed, no AssertionError raised.")
except AssertionError as e:
    print_stacktrace(e)
```
This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0 and print "Issue is fixed, no AssertionError raised.".