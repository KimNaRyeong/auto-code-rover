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
    exit(1)

print("Issue reproduced successfully. The issue is present.")
exit(0)
```

This script will reproduce the issue by calling `da.quantile(.9, dim='x', keep_attrs=True)` and checking if the resulting DataArray has any attributes. If not, it raises an AssertionError with a message indicating that the issue is present.