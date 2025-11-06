Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from io import StringIO

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
    da.quantile(q=200)  # This is the line that should raise an error
except ValueError as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
```

This script will attempt to reproduce the issue by calling `da.quantile(q=200)`. If the issue is present, it will catch the `ValueError` exception and print a stack trace. Then, it will raise an `AssertionError` to indicate that the issue was not fixed.

If you run this script and the issue is still present, it should print the stack trace of the error and exit with code 1. If the issue is fixed, it should simply print "Issue not fixed" and exit with code 0.