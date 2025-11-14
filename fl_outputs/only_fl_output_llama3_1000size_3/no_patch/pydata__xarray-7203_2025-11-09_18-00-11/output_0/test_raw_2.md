Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import xarray as xr
import time
from functools import wraps

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        if end_time - start_time > 36.4:  # adjust this value based on the expected time
            raise AssertionError("Repr takes too long")
        return result
    return wrapper

@timing
def reproduce_issue():
    dc1 = xr.open_dataset('s3://its-live-data/datacubes/v02/N40E080/ITS_LIVE_vel_EPSG32645_G0120_X250000_Y4750000.zarr', engine='zarr', storage_options={'anon': True})
    return dc1._repr_html_()

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Reproducer finished successfully.")
exit(0)
```

This script uses a decorator `timing` to measure the time taken by the function `reproduce_issue`. If the time taken exceeds 36.4 seconds, it raises an `AssertionError`. The script then attempts to execute the `reproduce_issue` function and prints a stack trace if any exception occurs.