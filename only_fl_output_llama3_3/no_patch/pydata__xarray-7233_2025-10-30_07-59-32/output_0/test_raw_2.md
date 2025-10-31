I apologize for the mistake earlier. Here is a new reproducer script that should reproduce the issue:

```python
import xarray as xr
import numpy as np

def main():
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    try:
        ds_coarsened = ds.coarsen(time=12).construct({"time": "month"})
        assert not hasattr(ds_coarsened.coords, "day")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will check if the `day` coordinate is still present after coarsening and constructing the dataset. If it is, an `AssertionError` will be raised with a stack trace.