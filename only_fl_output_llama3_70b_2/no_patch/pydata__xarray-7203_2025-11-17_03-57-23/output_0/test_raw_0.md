Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import xarray as xr
import time
from datetime import timedelta

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
    dc1 = xr.open_dataset('s3://its-live-data/datacubes/v02/N40E080/ITS_LIVE_vel_EPSG32645_G0120_X250000_Y4750000.zarr', engine='zarr', storage_options={'anon':True})
    start_time = time.time()
    dc1._repr_html_()
    end_time = time.time()
    elapsed_time = timedelta(seconds=end_time - start_time)
    print(f"Repr took {elapsed_time}")
    assert elapsed_time.total_seconds() < 10, "Repr took too long"
except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)

print("Repr was fast enough")
```
This script will try to reproduce the issue by loading the dataset and calling `_repr_html_()` on it. It measures the time taken for this operation and asserts that it took less than 10 seconds. If the assertion fails, it prints a stack trace of the exception and exits with code 1. If the assertion passes, it prints a success message and exits with code 0.