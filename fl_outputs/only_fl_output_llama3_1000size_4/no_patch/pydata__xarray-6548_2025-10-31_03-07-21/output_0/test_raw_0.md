Here is the reproducer script:

```Python
import xarray as xr
import traceback
import sys

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
    coeffs = xr.DataArray([1, 2, 3], dims="degree")
    coord = xr.DataArray([0, 1, 2], dims="x")
    xr.polyval(coord, coeffs)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected xr.polyval to work with unnamed coordinate")

try:
    import xarray as xr
    coeffs = xr.DataArray([1, 2, 3], dims="degree")
    coord = xr.DataArray([0, 1, 2], dims="x", name="x")
    xr.polyval(coord, coeffs)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected xr.polyval to work with named coordinate")

print("Test passed.")
```

This script will first try to evaluate the polynomial at the given points without a name for the coordinate. This should raise an exception and print the stack trace. Then it will try to do the same thing but this time giving a name to the coordinate. If this works, then the test passes.