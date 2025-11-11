Here is the reproducer script:

```python
import xarray as xr
import os
import sys
from functools import wraps

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

def reproducer():
    url = "https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/swot_adac/FESOM/surf/fma.zarr"
    ds = xr.open_dataset(url, engine='zarr')
    try:
        ds.chunks
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproducer()
```

This script will attempt to open the specified Zarr dataset using `xarray`, and then access the `chunks` attribute. If an exception is raised, it will print the stack trace and exit with code 1.