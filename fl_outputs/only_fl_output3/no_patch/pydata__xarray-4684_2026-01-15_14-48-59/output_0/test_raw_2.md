Based on the requirements, I've prepared a standalone Python file named `reproducer.py` to demonstrate how to programmatically check for the reported issue with datetime64 precision loss during an I/O roundtrip using `xarray`. This script checks for the condition described in the issue (losing millisecond precision after saving and reloading a file) and uses the provided function for printing the stack trace clearly if an `AssertionError` occurs due to the issue being present.

Please ensure that xarray and all its dependencies are correctly installed in your environment before running this script. The script assumes a basic familiarity with Python's filesystem operations for handling the creation and deletion of temporary files.

```python
import numpy as np
import xarray as xr
import tempfile
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

def test_roundtrip_precision():
    time_data = np.array(['2017-02-22T16:24:10.586000000'], dtype='datetime64[ns]')
    data = xr.DataArray(time_data, dims=['time'])

    # Create a temporary netcdf file
    with tempfile.NamedTemporaryFile(suffix='.nc', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        data.to_netcdf(tmp_path)
        loaded_data = xr.load_dataarray(tmp_path)

        before_disk_ts = data.sel(time=0).values
        after_disk_ts = loaded_data.sel(time=0).values

        assert before_disk_ts == after_disk_ts, "Datetime precision lost during IO roundtrip"

    except AssertionError as e:
        print_stacktrace(e)
        raise
    finally:
        # Clean up the temporary file
        os.remove(tmp_path)

if __name__ == '__main__':
    test_roundtrip_precision()
```

This script achieves the following:
- Creates an `xarray.DataArray` object with datetime64 data to emulate the issue scenario.
- Saves the `DataArray` to a temporary NetCDF file on disk.
- Loads this data back into another `DataArray` object.
- Checks if there's a loss in datetime precision by comparing datetime values before and after the disk I/O roundtrip.
- Uses the `print_stacktrace` function to print detailed error information if the assertion fails, indicating the presence of the issue.

Once the issue is fixed, running this script should not produce any output and should exit with code 0, indicating the absence of the issue.