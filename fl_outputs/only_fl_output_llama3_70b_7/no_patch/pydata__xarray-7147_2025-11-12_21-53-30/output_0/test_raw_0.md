Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import xarray as xr
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
ds = xr.merge([valid_times, invalid_times])

try:
    xr.decode_cf(ds)
except Exception as e:
    print_stacktrace(e)
    assert "unable to decode time units 'days since 0001-01-01' with calendar 'noleap'" in str(e), "Error message does not indicate the problematic variable's name"
    raise AssertionError("Issue is present: Time decoding error message does not include the problematic variable's name")
```
This script will raise an `AssertionError` when the issue is present, and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.