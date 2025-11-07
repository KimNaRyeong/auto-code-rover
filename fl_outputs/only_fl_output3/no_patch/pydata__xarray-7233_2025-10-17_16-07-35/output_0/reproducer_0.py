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

def reproduce_issue():
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    result = ds.coarsen(time=12).construct(time=("year", "month"))

    assert "day" in result.coords, "Expected 'day' to be in coordinates but it was demoted to a variable."

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue did not occur. Exiting with code 0.")
exit(0)
