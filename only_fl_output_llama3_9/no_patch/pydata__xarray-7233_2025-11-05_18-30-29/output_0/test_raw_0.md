Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from assertpy import assert_that

def main():
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    try:
        ds_coarsened = ds.coarsen(time=12).construct(time=("year", "month"))
        assert_that(ds_coarsened.coords["day"].dims, equal_to(["year", "month"]))
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will run the reproducer and if the issue is present, it will print a stack trace and exit with code 1. If the issue is fixed, it will simply exit with code 0.