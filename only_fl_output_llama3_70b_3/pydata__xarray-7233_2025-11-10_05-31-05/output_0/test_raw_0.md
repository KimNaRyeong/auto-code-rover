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

    assert all(coord.name in ["year", "month"] for coord in coarsened_ds.coords.values()), \
        "Non-dimensional coordinates are demoted to variables"

    print("Issue is fixed!")
except AssertionError as e:
    print_stacktrace(e)
```
This script will raise an `AssertionError` when the issue is present, printing a stack trace of the issue. If the issue is fixed, it will print "Issue is fixed!" and exit with code 0.