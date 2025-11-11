Here is the reproducer script:

```Python
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
    coord = xr.DataArray([0, 1, 2], dims="x")
    xr.polyval(coord, np.array([1, 2, 3]))
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected the issue to be reproduced")
```

This script will try to evaluate a polynomial at some points using `xr.polyval`. If the issue is present, it should raise an exception and print a stack trace.