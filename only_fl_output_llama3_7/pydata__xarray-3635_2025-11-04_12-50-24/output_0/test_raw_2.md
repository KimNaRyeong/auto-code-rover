I apologize for the mistake earlier. Here is a new reproducer script that should reproduce the issue:

```python
import xarray as xr
import numpy as np

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
    da.quantile(q=150)  # This should raise a ValueError
except ValueError as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
else:
    print("Issue not reproduced")
    exit(0)
```

This script will attempt to reproduce the issue by calling `da.quantile(q=150)` which should raise a `ValueError` with the message "Percentiles must be in the range [0, 100]". If this happens, it will print the stack trace and then raise an `AssertionError` to indicate that the issue was successfully reproduced.