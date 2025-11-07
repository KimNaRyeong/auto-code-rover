Certainly! Below is the `reproducer.py` script tailored to reproduce the specific problem you outlined regarding `xr.polyval`. Please ensure this script is executed in an environment that closely matches the versions and setup you've described to avoid unrelated errors.

```python
# reproducer.py

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

def test_xr_polyval_requires_name_attribute():
    import xarray as xr

    coeffs = xr.DataArray([1, 2, 3], dims="degree")
    coord = xr.DataArray([0, 1, 2], dims="x")
    coord2 = xr.DataArray([0, 1, 2], dims="x", name="x")

    try:
        xr.polyval(coord, coeffs)
        raise AssertionError("xr.polyval did not raise an error when it should have due to missing name attribute.")
    except KeyError as e:
        # Expected path for the issue
        print("Correctly caught KeyError due to missing name attribute.")
    
    try:
        result = xr.polyval(coord2, coeffs)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected error when calling xr.polyval with named coordinate.")
    else:
        print("xr.polyval works as expected with coord having a proper name.")

if __name__ == "__main__":
    test_xr_polyval_requires_name_attribute()
    print("Test completed. If no AssertionError was raised, then the test scenario ran as expected.")
```

This script performs two tests:
1. It attempts to use `xr.polyval` with a coordinate array that lacks a `name` attribute, expecting to catch a `KeyError`. This reproduces the described issue.
2. It then tests the function with a coordinate array that has a `name` attribute corresponding to its dimension, which should work correctly according to your description.

Upon execution, the script should raise an `AssertionError` if `xr.polyval` behaves differently than expected in the issue description or if there's an unexpected exception during the second test. Conversely, it prints messages to indicate the expected failures or successful completions of each step, aiming to confirm the behavior described in your issue.