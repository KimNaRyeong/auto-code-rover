Here is the reproducer script:

```Python
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

try:
    import xarray as xr
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Failed to import xarray")

coeffs = xr.DataArray([1, 2, 3], dims="degree")

# With a "handmade" coordinate it fails:
coord = xr.DataArray([0, 1, 2], dims="x")

try:
    xr.polyval(coord, coeffs)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected xr.polyval to work with handmade coordinates")
```

This script will try to import xarray and then attempt to use `xr.polyval` with a "handmade" coordinate. If any of these operations fail, it will print the stack trace and raise an `AssertionError`.