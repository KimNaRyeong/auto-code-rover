Here is the reproducer script:

```python
import xarray as xr
import pickle
import os

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
    with open('bug_data.p', 'rb') as f:
        data = pickle.load(f)

    selector = dict(animal=0, timepoint=0, wavelength='410', pair=0)
    before_disk_ts = data.time.sel(**selector).values[()]

    data.time.encoding = {'units': 'microseconds since 1900-01-01', 'calendar': 'proleptic_gregorian'}

    data.to_netcdf('test.nc')
    after_disk_ts = xr.load_dataarray('test.nc').time.sel(**selector).values[()]

    print(f'before roundtrip: {before_disk_ts}')
    print(f'after roundtrip: {after_disk_ts}')

    if before_disk_ts != after_disk_ts:
        raise AssertionError("Issue reproduced")

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
exit(0)
```

This script should be run in the same directory where `bug_data.p` is located.