Here is a new standalone Python file `reproducer.py` that should reproduce the original issue:
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
    da = xr.DataArray([0, 1, 2])
    da.quantile(q=50)
except ValueError as e:
    if str(e) == "Percentiles must be in the range [0, 100]":
        print_stacktrace(e)
        assert False, "Issue is present: incorrect error message"
    else:
        print("Error message is correct:", str(e))
```
This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

Please note that I've updated the error message in the `except` block to match the original error message "Percentiles must be in the range [0, 100]".