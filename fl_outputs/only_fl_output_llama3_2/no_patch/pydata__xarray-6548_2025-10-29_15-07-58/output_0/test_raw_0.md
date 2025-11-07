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
    coeffs = xr.DataArray([1, 2, 3], dims="degree")
    coord = xr.DataArray([0, 1, 2], dims="x")
    xr.polyval(coord, coeffs)
except Exception as e:
    print_stacktrace(e)
    raise

print("Issue not present. Exiting with code 0.")
exit(0)
```

This script will attempt to reproduce the issue by calling `xr.polyval` with a DataArray that does not have a name attribute. If an exception is raised, it will print the stack trace and then re-raise the exception.