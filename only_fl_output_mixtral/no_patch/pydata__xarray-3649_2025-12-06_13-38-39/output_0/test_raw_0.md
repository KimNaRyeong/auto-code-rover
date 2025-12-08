 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import numpy as np
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x1 = xr.Dataset(
     {"temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))}
     , coords={"y": [0, 1], "x": [10, 20, 30]}
)
x2 = xr.Dataset(
     {"temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))}
     , coords={"y": [2, 3], "x": [10, 20, 30]}
)
x3 = xr.Dataset(
     {"temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))}
     , coords={"y": [2, 3], "x": [40, 50, 60]}
)

try:
    result = xr.combine_by_coords([x1,x2,x3])
except Exception as e:
    print_stacktrace(e)
```

This script will reproduce the issue and print the stack trace when executed by `python3 reproducer.py`.