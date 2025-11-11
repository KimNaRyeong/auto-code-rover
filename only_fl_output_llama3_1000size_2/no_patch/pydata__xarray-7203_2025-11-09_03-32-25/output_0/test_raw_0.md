Here is the reproducer script:

```Python
import xarray as xr
import os
import time

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

def reproduce_issue():
    try:
        dc1 = xr.open_dataset('s3://its-live-data/datacubes/v02/N40E080/ITS_LIVE_vel_EPSG32645_G0120_X250000_Y4750000.zarr', engine='zarr', storage_options={'anon': True})
        start_time = time.time()
        _ = dc1._repr_html_()
        end_time = time.time()
        if end_time - start_time > 30:  # adjust the threshold as needed
            raise AssertionError("Repr takes too long")
    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to open a dataset, generate its repr, and check if it takes more than 30 seconds. If the repr generation takes longer than that, an `AssertionError` is raised with a stack trace printed.