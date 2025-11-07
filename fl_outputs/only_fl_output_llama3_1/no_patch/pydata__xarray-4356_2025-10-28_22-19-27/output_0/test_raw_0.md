Here is the reproducer script:

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
    da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
    da.sum(["dim_0", "dim_1"], min_count=1)
except AssertionError as e:
    print_stacktrace(e)
    raise
finally:
    if not isinstance(sys.last_traceback, type(None)):
        print("Issue is present")
        sys.exit(1)
    else:
        print("Issue is fixed")
        sys.exit(0)
```

This script will reproduce the issue by calling `da.sum` with `min_count=1` and more than one dimension. If the issue is present, it will print a stack trace and exit with code 1. If the issue is fixed, it will print "Issue is fixed" and exit with code 0.