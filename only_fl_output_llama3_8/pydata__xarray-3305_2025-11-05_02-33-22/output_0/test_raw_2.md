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
    da = xr.DataArray([0, 0], dims="x", attrs={'units':'K'})
    out = da.quantile(.9, dim='x', keep_attrs=True)
    assert out.attrs == {'units': 'K'}
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue reproduced successfully.")
sys.exit(0)
```

This script will attempt to reproduce the issue by creating a DataArray and then calling its `quantile` method. If the issue is present, it will raise an AssertionError. The script then prints a stack trace of the exception using the provided function.