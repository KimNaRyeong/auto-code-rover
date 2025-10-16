# reproducer.py
import xarray as xr
import numpy as np

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

def check_coordinates_remain(ds_before, ds_after):
    """
    Checks if all coordinates that were present before an operation are still present after.
    """
    before_coords = set(ds_before.coords.keys())
    after_coords = set(ds_after.coords.keys())
    
    if not before_coords.issubset(after_coords):
        raise AssertionError("Some coordinates have been demoted to variables.")

try:
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    ds_before = ds
    ds_after = ds.coarsen(time=12).construct(time=("year", "month"))

    check_coordinates_remain(ds_before, ds_after)
    print("Coordinates correctly preserved after coarsening and constructing.")
except AssertionError as e:
    print_stacktrace(e)
    raise

