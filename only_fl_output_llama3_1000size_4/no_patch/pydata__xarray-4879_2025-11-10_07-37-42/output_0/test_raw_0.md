Here is the reproducer script:

```python
import xarray as xr
from pathlib import Path
import numpy as np
import os
import unittest

def test_repr(nx):
    ds = xr.DataArray(np.random.rand(nx))
    path = Path("saved_on_disk.nc")
    if path.exists():
        path.unlink()
    ds.to_netcdf(path)
    return path

class TestReproducer(unittest.IsolatedTestCase):
    def test_reproducer(self):
        os.environ['JUPYTER_NOTEBOOK_NAME'] = 'test_notebook'
        test_repr(4)
        print(xr.open_dataset("saved_on_disk.nc"))
        test_repr(5)
        print(xr.open_dataset("saved_on_disk.nc"))

        with self.assertRaises(AssertionError):
            xr.open_dataset("saved_on_disk.nc")

if __name__ == '__main__':
    try:
        test_reproducer()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

```

This script will run the `test_repr` function twice, then attempt to open the netcdf file again. If the issue is present, it should raise an `AssertionError`, which we catch and print a stack trace for.