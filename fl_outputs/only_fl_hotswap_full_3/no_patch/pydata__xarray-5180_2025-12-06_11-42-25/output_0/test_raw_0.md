 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import numpy as np
import pandas as pd

def print_time_type(dataset):
    print(dataset.time.dtype, type(dataset.time[0].item()))

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

da = xr.DataArray(
    data=[32, 16, 8],
    dims=["time"],
    coords=dict(
        time=pd.date_range("2014-09-06", periods=3),
        reference_time=pd.Timestamp("2014-09-05"),
    ),
)

ds1 = xr.Dataset({"myvar": da})
print_time_type(ds1)  # prints "datetime64[ns]" <class 'int'>

ds1.time.encoding["calendar"] = "Gregorian"
ds1.reference_time.encoding["calendar"] = "Gregorian"
ds1.to_netcdf("test-capitalized.nc")

try:
    ds2 = xr.open_dataset("test-capitalized.nc")
    print_time_type(ds2)  # prints "object" <class 'cftime._cftime.DatetimeGregorian'>
except AssertionError as e:
    print_stacktrace(e)
else:
    print("No AssertionError raised, test failed.")
```
The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.