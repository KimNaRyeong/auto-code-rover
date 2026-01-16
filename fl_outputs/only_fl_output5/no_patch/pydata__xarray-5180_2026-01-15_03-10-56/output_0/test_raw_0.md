```python
# reproducer.py
import xarray as xr
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

def check_time_type(dataset):
    "Check and assert the time co-ordinate type of the dataset."
    dtype_str = str(dataset.time.dtype)
    first_item_type = type(dataset.time[0].item())
    expected_dtype_str = "datetime64[ns]"
    expected_first_item_type = pd.Timestamp
    assert dtype_str == expected_dtype_str, f"Expected dtype: {expected_dtype_str}, got: {dtype_str}"
    assert first_item_type == expected_first_item_type, f"Expected first item type: {expected_first_item_type}, got: {first_item_type}"

try:
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
    check_time_type(ds1)  # should pass without issue

    # Manually set time attributes to "Gregorian"
    ds1.time.encoding["calendar"] = "Gregorian"
    ds1.reference_time.encoding["calendar"] = "Gregorian"
    ds1.to_netcdf("test-capitalized.nc")

    ds2 = xr.open_dataset("test-capitalized.nc")
    check_time_type(ds2)  # this should raise an AssertionError if the issue is present
    print("Issue not present, test passed.")

except AssertionError as e:
    print_stacktrace(e)
    raise e

finally:
    import os
    if os.path.exists("test-capitalized.nc"):
        os.remove("test-capitalized.nc")
```