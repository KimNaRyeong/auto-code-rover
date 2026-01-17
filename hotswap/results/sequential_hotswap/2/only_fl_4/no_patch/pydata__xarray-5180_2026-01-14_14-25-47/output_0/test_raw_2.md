```python
import xarray as xr
import pandas as pd
import numpy as np

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

def main():
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
        ds1.time.encoding["calendar"] = "Gregorian"
        ds1.reference_time.encoding["calendar"] = "Gregorian"

        ds1.to_netcdf("test-capitalized.nc")

        ds2 = xr.open_dataset("test-capitalized.nc")

        assert np.issubdtype(ds2.time.dtype, np.datetime64), "Expected time coordinate to be numpy datetime64 type"
        assert type(ds2.time.values[0]) is np.datetime64, "Expected elements of time coordinate to be numpy datetime64 instances"

        print("Test passed: time coordinate is represented as numpy datetime64.")

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        exit(1)
    exit(0)
```