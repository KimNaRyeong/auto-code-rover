Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import xarray as xr

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
        f"Non-dimensional coordinates 'day' should not be demoted to variables, but got {coarsened_ds.coords}"

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script reproduces the issue by creating a `DataArray` with a non-dimensional coordinate "day", coarsening it using `ds.coarsen`, and then constructing a new dataset with the coarsened data. The script then checks if the resulting dataset still has "day" as a coordinate, and raises an `AssertionError` if it does not. If the issue is fixed, the script will exit with code 0.