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

    try:
        coeffs = xr.DataArray([1, 2, 3], dims="degree")
        # Case 1: Coord without name
        coord = xr.DataArray([0, 1, 2], dims="x")
        # This is expected to raise a KeyError due to missing name attribute
        xr.polyval(coord, coeffs)
    except KeyError as e:
        print_stacktrace(e)
    else:
        raise AssertionError("Expected KeyError was not raised")

    try:
        # Case 2: Coord with name, matching the dimension
        coord_with_name = xr.DataArray([0, 1, 2], dims="x", name="x")
        # This should work without errors
        xr.polyval(coord_with_name, coeffs)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected error occurred")
    else:
        print("No issues detected.")

if __name__ == "__main__":
    main()
```