```python
import numpy as np
import xarray as xr

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

def test_coarsen_keeps_coordinates():
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    # Expected: the 'day' coordinate should stay as a coordinate after coarsen.construct
    coarse_ds = ds.coarsen(time=12).construct(time=("year", "month"))

    # Verifying that 'day' remains as a coordinate
    if not set(coarse_ds.coords).issuperset({"day"}):
        raise AssertionError("The 'day' variable was demoted from a coordinate to a variable.")

try:
    test_coarsen_keeps_coordinates()
except AssertionError as e:
    print_stacktrace(e)
    # This exception is expected when the issue is present. It indicates a failure in the test.
    sys.exit(1)  # Exiting with error to signal failure
else:
    print("The issue appears to be resolved.")  # No error, so the issue might have been fixed

sys.exit(0)  # Exiting with success when there's no AssertionError
```

This script tests for the specific issue discussed regarding `ds.Coarsen.construct` behavior in xarray: where it's reported that non-dimensional coordinates are demoted to variables instead of being kept as coordinates. This script will fail (raising an `AssertionError` and providing a stack trace) if the issue is present, thereby acting as an automated test for this issue. 

When you run `python3 reproduducer.py` in the project root directory, it will verify whether the issue remains or not by checking that coordinates before and after `coarsen.construct` maintain their status.