Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    ds = xr.open_dataarray('test.nc', engine='h5netcdf')
    ds.to_zarr('test.zarr', compute=True)
    ds_loaded = xr.open_zarr('test.zarr')
    xr.decode_cf(ds_loaded)
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("Decode_cf fails when scale_factor is a length-1 list")
```
This script creates a NetCDF file `test.nc` with `scale_factor` and `add_offset` encoded as length-1 lists, writes it to Zarr using the `h5netcdf` engine, loads the Zarr dataset, and then calls `xr.decode_cf(ds_loaded)`. If the issue is present, an `AttributeError` will be raised, and the script will print the stack trace using the provided function. If the issue is fixed, the script will exit with code 0.

To run this script, you need to create a NetCDF file `test.nc` with the required attributes. You can use a tool like `ncks` or `ncgen` to create such a file.

Please note that this script assumes that the `h5netcdf` engine is installed and available. If not, you may need to install it using `conda` or `pip`.