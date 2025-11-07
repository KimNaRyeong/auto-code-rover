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
    da.quantile(q=50.5)
except ValueError as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
```

This script will reproduce the issue by calling `da.quantile(q=50.5)`, which should raise a `ValueError` with the message "Percentiles must be in the range [0, 100]". The script then prints the stack trace and raises an `AssertionError` to indicate that the issue was reproduced.