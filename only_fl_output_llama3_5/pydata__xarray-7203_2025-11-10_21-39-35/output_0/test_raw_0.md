Here is the reproducer script:

```Python
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

def reproducer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)
    return wrapper

@reproducer
def main():
    dc1 = xr.open_dataset('s3://its-live-data/datacubes/v02/N40E080/ITS_LIVE_vel_EPSG32645_G0120_X250000_Y4750000.zarr', engine='zarr', storage_options={'anon': True})
    dc1._repr_html_()

if __name__ == "__main__":
    main()
```

This script will reproduce the issue by calling `dc1._repr_html_()` and print a stack trace if an `AssertionError` is raised.