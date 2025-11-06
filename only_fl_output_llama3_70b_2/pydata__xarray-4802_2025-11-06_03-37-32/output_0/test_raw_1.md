Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import numpy as np
from xarray.backends import HDF5Backend, ZarrBackend

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
    # Create a dataset with scale_factor as a length-1 list
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()

    # Write the dataset to Zarr
    ds.to_zarr('temp.zarr', mode='w')

    # Read the dataset from Zarr
    with ZarrBackend('temp.zarr') as store:
        ds_read = xr.open_zarr(store)

    # Try to decode the dataset using CF conventions
    xr.decode_cf(ds_read)
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("Decode_cf fails when scale_factor is a length-1 list")
```
This script creates a `DataArray` with `scale_factor` and `add_offset` encoded as length-1 lists, writes it to Zarr, reads it back from Zarr, and then tries to decode it using CF conventions. If the issue is present, an `AttributeError` will be raised, and the script will print the stack trace of the error and raise an `AssertionError`. If the issue is fixed, the script will exit with code 0.