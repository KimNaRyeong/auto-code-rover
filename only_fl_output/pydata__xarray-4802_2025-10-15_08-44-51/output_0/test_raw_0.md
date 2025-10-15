```python
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
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()
    xr.decode_cf(ds)
    print("The issue is fixed.")
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("The issue is present.") from e
```

This script checks for the specific failure in decoding CF conventions when `scale_factor` and `add_offset` attributes are provided as length-1 lists instead of single values. If the issue is present, it prints a detailed stack trace of where the problem occurs and raises an `AssertionError`. Conversely, if the issue has been resolved, it prints a success message and exits with code 0.