```python
# reproducer.py

import xarray as xr
import pandas as pd
import numpy as np
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
    filename = "test-capitalized.nc"
    ds1.to_netcdf(filename)

    try:
        ds2 = xr.open_dataset(filename)
        dtype, type_of_first_item = ds2.time.dtype, type(ds2.time.values[0])
        
        # Correct the assertion to match the expected failure condition
        assert dtype == np.dtype('datetime64[ns]'), f"Unexpected dtype: {dtype}"
        assert isinstance(type_of_first_item, pd.Timestamp), f"Unexpected type of first item: {type_of_first_item}"

        print("Test passed: No issues found.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    except Exception as e:
        print_stacktrace(e)
        exit(1)
    
    finally:
        os.remove(filename)

if __name__ == "__main__":
    main()
```

This script aims to reproduce the reported issue by creating a sample dataset with a 'Gregorian' calendar attribute, saving it as a NetCDF file, then loading it to verify the type of the time coordinate and its first value. The assertion checks have been adjusted to specifically catch the condition described in the bug report. Errors or failed assertions will result in a stack trace being printed to aid in diagnosing the issue.