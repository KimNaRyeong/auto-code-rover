 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import xarray as xr
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    expected_ds = ds.copy()

    try:
        result_ds = ds.coarsen(time=12).construct(time=("year", "month"))
        assert result_ds.dims == expected_ds.dims
        assert result_ds.coords == expected_ds.coords
        assert result_ds.data_vars == expected_ds.data_vars
    except AssertionError:
        print_stacktrace(AssertionError("Coordinates were demoted to variables after coarsening."))
        raise
```

This script defines a `print_stacktrace` function to print the stack trace when an `AssertionError` is raised. The script then creates a `DataArray` with a non-dimensional coordinate `day`, converts it to a `Dataset`, and coarsens it. The resulting `Dataset` is compared to the expected `Dataset`, and if there are any differences, an `AssertionError` is raised with a stack trace.

To execute the script, run `python3 reproducer.py` in the root directory of the project. If the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will exit with code 0.