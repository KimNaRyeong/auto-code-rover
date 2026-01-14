 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

da = xr.DataArray([0, 0], dims="x", attrs={'units':'K'})
out = da.quantile(.9, dim='x', keep_attrs=True)
expected_attrs = {'units': 'K'}
try:
    assert out.attrs == expected_attrs
except AssertionError as e:
    print_stacktrace(e)
```
When the issue is present, the script will raise an `AssertionError` and print a stack trace of the issue. When the issue is fixed, the script will exit with code 0.