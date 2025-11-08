Here is the reproducer script:

```python
import xarray as xr
import numpy as np
import pandas as pd

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
        da = xr.DataArray(
            data=[32, 16, 8],
            dims=["time"],
            coords=dict(
                time=pd.date_range("2014-09-06", periods=3),
                reference_time=pd.Timestamp("2014-09-05"),
            ),
        )

        ds1 = xr.Dataset({"myvar": da})
        print(ds1.time.dtype, type(ds1.time[0].item()))

        ds1.time.encoding["calendar"] = "Gregorian"
        ds1.reference_time.encoding["calendar"] = "Gregorian"
        ds1.to_netcdf("test-capitalized.nc")

        ds2 = xr.open_dataset("test-capitalized.nc")
        print(ds2.time.dtype, type(ds2.time[0].item()))

    except Exception as e:
        print_stacktrace(e)

reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.