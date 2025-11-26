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
    # Create a sample dataset
    data = xr.DataArray([0, 1, 2], name='foo',
                        attrs={'scale_factor': [0.01],
                               'add_offset': [1.0]}).to_dataset()

    # Write the dataset to HDF5 file
    data.to_netcdf('temp.nc', engine='h5netcdf')

    # Read the dataset from HDF5 file using h5netcdf engine
    ds_h5 = xr.open_dataarray('temp.nc', engine='h5netcdf')

    # Write the dataset to Zarr store
    ds_h5.to_zarr('temp.zarr', consolidated=True)

    # Read the dataset from Zarr store
    ds_zarr = xr.open_zarr('temp.zarr', engine=ZarrBackend())

    # Try to decode CF conventions
    xr.decode_cf(ds_zarr)

except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("Decode_cf fails when scale_factor is a length-1 list")
```
This script creates a sample dataset, writes it to an HDF5 file using the `h5netcdf` engine, reads it back, writes it to a Zarr store, reads it back from the Zarr store, and then tries to decode CF conventions. If the issue is present, an `AttributeError` will be raised, and the script will print the stack trace using the provided `print_stacktrace` function. The script will also raise an `AssertionError` with a message indicating that the issue is still present.

If the issue is fixed, the script will exit with code 0 without raising any errors.