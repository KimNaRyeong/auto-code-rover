Here is the reproducer script:

```python
import xarray as xr
from pathlib import Path
import numpy as np
import os

def test_repr(nx):
    ds = xr.DataArray(np.random.rand(nx))
    path = Path("saved_on_disk.nc")
    if path.exists():
        path.unlink()
    ds.to_netcdf(path)
    return path

def reproduce_issue():
    try:
        # Create a new file
        test_repr(4)

        # Open the file and print it
        print(xr.open_dataset("saved_on_disk.nc"))

        # Create another file
        test_repr(5)

        # Open the file again, but this time use repr to display the xarray object
        xr.open_dataset("saved_on_disk.nc")

        # Now, open the file again and check if it still shows the wrong data
        assert xr.open_dataset("saved_on_disk.nc") == xr.open_dataset("saved_on_disk.nc"), "Issue reproduced"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates two files, opens them, and then uses `repr` to display the xarray object. It checks if the file still shows the wrong data after using `repr`. If it does, an `AssertionError` is raised, which is caught by the script and prints a stack trace before exiting with code 1.