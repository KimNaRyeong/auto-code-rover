Here is the reproducer script:

```Python
import xarray as xr
import numpy as np
from io import StringIO
import sys
import traceback

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
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    ds.coarsen(time=12).construct(time=("year", "month"))
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not reproduced")
sys.exit(0)
```

This script will raise an `AssertionError` if the issue is present, and it will print a stack trace of the issue. If the issue is fixed, it will simply print "Issue not reproduced" and exit with code 0.