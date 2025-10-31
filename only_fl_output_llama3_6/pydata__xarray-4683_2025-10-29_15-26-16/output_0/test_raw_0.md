Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from typing import Any

def print_stacktrace(e: Exception) -> None:
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
    da = xr.DataArray([[1.0, 2.0], [3.0, 4.0]]).astype(dtype='d', order='F')
    da.values.strides
except TypeError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present")
exit(0)
```

This script tries to reproduce the issue by calling `astype` with the `order` parameter and then trying to access the `strides` attribute. If a `TypeError` is raised, it prints the stack trace and exits with code 1. Otherwise, it prints "Issue not present" and exits with code 0.