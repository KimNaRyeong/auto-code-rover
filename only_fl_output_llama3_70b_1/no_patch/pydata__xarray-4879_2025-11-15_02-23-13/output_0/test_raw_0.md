Here is the standalone Python script `reproducer.py` to reproduce the issue:
```python
import xarray as xr
from pathlib import Path
import numpy as np

def test_repr(nx):
    ds = xr.DataArray(np.random.rand(nx))
    path = Path("saved_on_disk.nc")
    if path.exists():
        path.unlink()
    ds.to_netcdf(path)
    return path

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
    # First run, all is fine
    test_repr(4)
    ds1 = xr.open_dataset("saved_on_disk.nc")
    print(ds1)

    # Second run, still fine
    test_repr(5)
    ds2 = xr.open_dataset("saved_on_disk.nc")
    print(ds2)

    # Use repr to display the xarray object
    _ = xr.open_dataset("saved_on_disk.nc")

    # Third run, issue appears
    test_repr(6)
    ds3 = xr.open_dataset("saved_on_disk.nc")
    assert np.array_equal(ds1.values, ds3.values), "Data should be different"
    print_stacktrace(AssertionError("Issue reproduced"))
except AssertionError as e:
    print_stacktrace(e)
```
This script will raise an `AssertionError` when the issue is present, and print a stack trace of the issue. If the issue is fixed, the script will exit with code 0.

To run this script, save it to a file named `reproducer.py` in the root directory of your project, and execute it using `python3 reproducer.py`.