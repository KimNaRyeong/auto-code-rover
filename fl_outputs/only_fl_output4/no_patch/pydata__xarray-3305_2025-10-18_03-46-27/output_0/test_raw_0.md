```python
# reproducer.py
import xarray as xr
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_quantile_keeps_attrs():
    da = xr.DataArray([0, 0], dims="x", attrs={'units':'K'})
    out = da.quantile(.9, dim='x', keep_attrs=True)
    assert out.attrs == {'units': 'K'}, "quantile did not keep attributes"

if __name__ == "__main__":
    try:
        test_quantile_keeps_attrs()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    print("Issue not present, exited with code 0.")
    sys.exit(0)
```