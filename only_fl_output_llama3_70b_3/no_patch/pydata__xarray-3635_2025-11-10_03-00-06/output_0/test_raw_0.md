Here is the standalone Python file `reproducer.py` to reproduce the issue:
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
        raise AssertionError("Issue is present: incorrect error message")
    else:
        print("Error message is correct, issue is fixed.")
```
This script will raise an `AssertionError` with a stack trace when the issue is present, and exit with code 0 when the issue is fixed.