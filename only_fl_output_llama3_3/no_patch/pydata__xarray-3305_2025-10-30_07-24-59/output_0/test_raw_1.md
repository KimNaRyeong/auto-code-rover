Here is the reproducer script:

```python
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
    da = xr.DataArray([0, 0], dims="x", attrs={'units':'K'})
    out = da.quantile(.9, dim='x', keep_attrs=True)
    if not out.attrs:
        raise AssertionError("DataArray.quantile does not honor `keep_attrs`")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue reproduced successfully.")
sys.exit(0)
```

This script will attempt to reproduce the issue by calling `da.quantile(.9, dim='x', keep_attrs=True)`. If the output does not contain the expected attributes (`'units': 'K'`), it will raise an `AssertionError`, which is caught and printed with a stack trace.