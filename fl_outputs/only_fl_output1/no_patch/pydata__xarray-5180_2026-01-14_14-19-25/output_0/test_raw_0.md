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

def print_time_type(dataset):
    print(dataset.time.dtype, type(dataset.time[0].item()))

def main():
    import xarray as xr
    import pandas as pd

    da = xr.DataArray(
        data=[32, 16, 8],
        dims=["time"],
        coords=dict(
            time=pd.date_range("2014-09-06", periods=3),
            reference_time=pd.Timestamp("2014-09-05"),
        ),
    )

    ds1 = xr.Dataset({"myvar": da})
    # Initial check to ensure setup is correct, should raise no errors
    assert ds1.time.dtype == 'datetime64[ns]', f"Expected datetime64[ns], got {ds1.time.dtype}"
    
    ds1.time.encoding["calendar"] = "Gregorian"
    ds1.reference_time.encoding["calendar"] = "Gregorian"
    ds1.to_netcdf("test-capitalized.nc")

    ds2 = xr.open_dataset("test-capitalized.nc")
    try:
        assert not isinstance(ds2.time[0].item(), xr.coding.times.CFTimeIndex), "Time coordinate should not be CFTimeIndex when calendar is 'Gregorian'."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script setup a `xarray.Dataset` and modifies its calendar encoding to `"Gregorian"` before saving to a NetCDF file. Upon loading this file, the expected behavior is that the `time` coordinate should be represented using `datetime64[ns]` data type, following the Python pandas convention for representing dates and times within the broadly compatible Gregorian calendar. An `AssertionError` is raised with a detailed stack trace if the issue is present, indicating that `xarray` is decoding times into `cftime.datetime` objects instead of `np.datetime64[ns]` when it should not.