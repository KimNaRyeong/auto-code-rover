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
    if "Percentiles must be in the range [0, 100]" in str(e):
        print_stacktrace(e)
        assert False, "Issue is present"
    else:
        raise
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

Please note that I removed the `print("No issue found")` statement as it's not necessary in this case. Also, I added a `raise` statement to re-raise any other exceptions that might occur during execution.