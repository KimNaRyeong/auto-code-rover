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

def main():
    import xarray as xr

    da_with_units = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
    da_with_units.frequency.attrs["units"] = "GHz"

    try:
        initial_units = da_with_units.frequency.units
        da_without_units = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
        
        _ = da_with_units == da_without_units  # This is where the issue happens
        assert "units" in da_with_units.frequency.attrs, "The 'units' attribute was erased!"

        final_units = da_with_units.frequency.units
        assert initial_units == final_units, "The 'units' attribute was modified!"

    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
```

This script aims to identify and assert the bug described in the issue with xarray version 2022.6.0, where comparing two DataArrays using the built-in '==' operator leads to the unexpected mutation of the `attrs` dictionary of a `DataArray`. The script executes in a manner that isolates this specific behavior and verifies that the `attrs` dictionary remains unaltered before and after the comparison operation. If the issue persists, the script raises an `AssertionError` with a clear stack trace indicating the fault. Conversely, if the issue is fixed, the script will exit quietly with code 0, signalling the absence of the bug.