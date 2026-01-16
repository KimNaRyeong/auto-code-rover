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

def main():
    time_coord = pd.date_range("2020-01-01","2020-01-03", freq="12H")
    da = xr.DataArray([1, 2, 3, 4, 5], dims=["time"], coords={'time': time_coord})

    assert hasattr(da.time.dt, 'time'), "DatetimeAccessor missing 'time' attribute"

    try:
        assert hasattr(da.time.dt, 'date'), "DatetimeAccessor missing 'date' attribute"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit code 1 for errors

    print("No issues detected.")

if __name__ == "__main__":
    main()
```
This script checks for the presence of both the `time` and the (expected but missing) `date` attributes in the DatetimeAccessor of an xarray DataArray object. If the `date` attribute is missing, it catches the resulting `AssertionError`, prints a detailed stack trace using the `print_stacktrace` function, and exits with an error code to clearly indicate failure. When the issue is resolved, and both attributes are present without raising an AssertionError, it will print "No issues detected." and exit with code 0, indicating success.