Here is the reproducer script:

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

def main():
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    try:
        ds_coarsened = ds.coarsen(time=12).construct(time=("year", "month"))
        assert ds_coarsened.coords["day"].dims == ("time",), f"Expected day coordinates to be ({'time',}), got {ds_coarsened.coords['day'].dims}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will run the minimal complete verifiable example and then check if the coordinates of the coarsened dataset are still named `day` with dimensions `time`. If they are not, it will print a stack trace and raise an `AssertionError`.