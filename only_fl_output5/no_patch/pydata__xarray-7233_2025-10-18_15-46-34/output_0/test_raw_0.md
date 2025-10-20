```python
import xarray as xr
import numpy as np

def check_coarsen_construct_preserves_coordinates():
    # Create a DataArray and convert it to a Dataset with an additional coordinate
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    # Perform coarsen and construct operation
    coarsened_ds = ds.coarsen(time=12).construct(time=("year", "month"))

    # Check if the non-dimensional coordinates have been demoted to variables
    assert "day" in coarsened_ds.coords, "The 'day' coordinate has been demoted to a variable"

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

if __name__ == "__main__":
    try:
        check_coarsen_construct_preserves_coordinates()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    print("No issues detected.")
```

This script aims to reproduce the reported issue by performing a `coarsen` and `construct` operation on an `xarray.Dataset` that is expected to preserve non-dimensional coordinates as coordinates. The script checks if the `day` coordinate, which is a non-dimensional coordinate, remains as a coordinate after the operation. If `day` is demoted to a variable (indicating the issue is present), the script raises an `AssertionError` and prints a stack trace to provide detailed insight into where the failure occurred. If the issue is fixed and no assertion is raised, the script will print "No issues detected" and exit with code 0.