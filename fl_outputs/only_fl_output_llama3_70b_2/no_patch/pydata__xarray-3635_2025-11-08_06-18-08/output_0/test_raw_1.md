Here is the revised standalone Python file `reproducer.py` to reproduce the issue:
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
    if "Percentiles must be in the range [0, 100]" not in str(e):
        raise
    print_stacktrace(e)
    assert False, "Issue is present: Percentiles must be in the range [0, 100]"
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will exit with code 0 when the issue is fixed.

Please note that I've updated the exception handling to check if the error message contains "Percentiles must be in the range [0, 100]" and raise an `AssertionError` only if it does. If the error message is different, the original exception is re-raised.