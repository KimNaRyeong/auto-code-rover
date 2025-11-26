Here is the revised standalone Python script `reproducer.py` to reproduce the issue:
```
import xarray as xr
import numpy as np
import pandas as pd

def print_time_type(dataset):
    print(dataset.time.dtype, type(dataset.time[0].item()))

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

# Manually set time attributes to "Gregorian" rather
# than default "proleptic_gregorian".
ds1.time.encoding["calendar"] = "Gregorian"
ds1.reference_time.encoding["calendar"] = "Gregorian"
ds1.to_netcdf("test-capitalized.nc")

try:
    ds2 = xr.open_dataset("test-capitalized.nc")
    print_time_type(ds2)
    assert isinstance(ds2.time[0].item(), np.datetime64) or isinstance(ds2.time[0].item(), pd.Timestamp)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script should reproduce the issue and raise an `AssertionError` if the `time` coordinate is not represented as a `datetime64[ns]` or a `pd.Timestamp`.