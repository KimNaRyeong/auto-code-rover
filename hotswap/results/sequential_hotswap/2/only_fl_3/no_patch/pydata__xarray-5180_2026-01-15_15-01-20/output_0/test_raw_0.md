```python
import xarray as xr
import pandas as pd
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_time_type(dataset):
    dtype = dataset.time.dtype
    item_type = type(dataset.time[0].item())
    return dtype, item_type

def main():
    da = xr.DataArray(
        data=[32, 16, 8],
        dims=["time"],
        coords=dict(
            time=pd.date_range("2014-09-06", periods=3),
            reference_time=pd.Timestamp("2014-09-05"),
        ),
    )

    ds1 = xr.Dataset({"myvar": da})
    ds1.time.encoding["calendar"] = "Gregorian"
    ds1.reference_time.encoding["calendar"] = "Gregorian"
    ds1.to_netcdf("test-capitalized.nc")

    ds2 = xr.open_dataset("test-capitalized.nc")

    expected_dtype = 'datetime64[ns]'
    expected_item_type = pd.Timestamp

    try:
        dtype, item_type = check_time_type(ds2)
        
        # Verify the data type and item type against expected
        assert dtype == expected_dtype, f"Expected dtype {expected_dtype}, got {dtype}"
        assert item_type == expected_item_type, f"Expected item_type {expected_item_type}, got {item_type}"
        print(f"Issue fixed. Dtype is {dtype} and item type is {item_type.__name__}.")
        sys.exit(0)

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```