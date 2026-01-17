```python
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

def test_issue():
    import xarray as xr
    import pandas as pd
    import numpy as np

    def print_time_type(dataset):
        print(dataset.time.dtype, type(dataset.time[0].values))

    da = xr.DataArray(
        data=[32, 16, 8],
        dims=["time"],
        coords=dict(
            time=pd.date_range("2014-09-06", periods=3),
            reference_time=pd.Timestamp("2014-09-05"),
        ),
    )

    # Create dataset and confirm type of time
    ds1 = xr.Dataset({"myvar": da})
    print_time_type(ds1)  # prints "datetime64[ns]" <class 'numpy.datetime64'>

    # Manually set time attributes to "Gregorian"
    ds1.time.encoding["calendar"] = "Gregorian"
    ds1.reference_time.encoding["calendar"] = "Gregorian"
    ds1.to_netcdf("test-capitalized.nc")

    ds2 = xr.open_dataset("test-capitalized.nc")
    print_time_type(ds2)
    
    # Assert to check if the issue is present or fixed
    try:
        assert ds2.time.dtype == 'datetime64[ns]', "Issue is present: 'time' co-ordinate is not 'datetime64[ns]'"
        print("Issue fixed, exiting with code 0")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError:
        exit(1)
    exit(0)
```