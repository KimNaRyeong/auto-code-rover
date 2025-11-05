Here is the reproducer script:

```Python
import xarray as xr
import numpy as np
from unittest import TestCase

class TestCoarsenConstruct(TestCase):

    def test_coarsen_construct(self):
        da = xr.DataArray(np.arange(24), dims=["time"])
        da = da.assign_coords(day=365 * da)
        ds = da.to_dataset(name="T")

        try:
            ds.coarsen(time=12).construct(time=("year", "month"))
            self.fail("Expected AssertionError")
        except AssertionError as e:
            print_stacktrace(e)

if __name__ == "__main__":
    test_coarsen_construct()
```

This script will run the test case and raise an `AssertionError` if the issue is present. The stack trace of the error will be printed to the console.