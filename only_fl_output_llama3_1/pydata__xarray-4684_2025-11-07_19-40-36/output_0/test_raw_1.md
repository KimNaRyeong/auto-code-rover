Here is the reproducer script:

```python
import xarray as xr
import pickle
import os
from datetime import datetime, timedelta

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
    bug_data_path = 'bug_data.p'
    tmp_path = 'test.nc'

    with open(bug_data_path, 'rb') as f:
        data = pickle.load(f)

    selector = dict(animal=0, timepoint=0, wavelength='410', pair=0)

    before_disk_ts = data.time.sel(**selector).values[()]

    data.time.encoding = {'units': 'microseconds since 1900-01-01', 'calendar': 'proleptic_gregorian'}

    data.to_netcdf(tmp_path)
    after_disk_ts = xr.load_dataarray(tmp_path).time.sel(**selector).values[()]

    if before_disk_ts != after_disk_ts:
        raise AssertionError("Millisecond precision is lost on datetime64 during IO roundtrip")

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
finally:
    os.remove(tmp_path, exist_ok=True)
```

This script will load the pickle file, perform the same operations as in the original code, and then check if the before and after timestamps are equal. If they are not, it will raise an `AssertionError` with a stack trace.