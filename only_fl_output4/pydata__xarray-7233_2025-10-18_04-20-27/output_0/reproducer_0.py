# reproducer.py
import xarray as xr
import numpy as np

def check_coordinates_retained():
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")
    
    # Original dataset
    print("Original dataset:")
    print(ds)

    # Dataset after applying coarsen.construct
    coarsened_ds = ds.coarsen(time=12).construct(time=("year", "month"))
    print("\nCoarsened dataset:")
    print(coarsened_ds)

    # Check if 'day' coordinate is demoted to a variable
    if 'day' in coarsened_ds.variables and 'day' not in coarsened_ds.coords:
        raise AssertionError("Non-dimensional coordinate 'day' was demoted to a variable.")

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

if __name__ == '__main__':
    try:
        check_coordinates_retained()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("Issue not found. Exiting with code 0.")
    exit(0)
