Here is the standalone Python script `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import numpy as np
import os

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
    # Create a netCDF file with scale_factor as a length-1 list
    import netCDF4
    nc = netCDF4.Dataset('test.nc', 'w')
    foo = nc.createVariable('foo', 'f8', ())
    foo.scale_factor = [0.01]
    foo.add_offset = [1.0]
    nc.close()

    # Open the netCDF file using the h5netcdf engine
    ds = xr.open_dataset('test.nc', engine='h5netcdf')

    # Write the dataset to a Zarr store
    import zarr
    store = zarr.DirectoryStore('test.zarr')
    ds.to_zarr(store, consolidated=True)

    # Open the Zarr store and try to decode CF conventions
    ds = xr.open_zarr(store)
    xr.decode_cf(ds)
except AttributeError as e:
    print_stacktrace(e)
    assert False, "Decode_cf fails when scale_factor is a length-1 list"
finally:
    os.remove('test.nc')
    os.rmtree('test.zarr', ignore_errors=True)
```
This script creates a netCDF file with `scale_factor` and `add_offset` encoded as length-1 lists, opens it using the `h5netcdf` engine, writes it to a Zarr store, and then tries to decode CF conventions. If the issue is present, this will raise an `AttributeError`, which is caught by the `except` block. The script prints the stack trace of the error using the provided `print_stacktrace` function and then raises an `AssertionError` with a message indicating that the issue is still present. If the issue is fixed, the script will exit with code 0.