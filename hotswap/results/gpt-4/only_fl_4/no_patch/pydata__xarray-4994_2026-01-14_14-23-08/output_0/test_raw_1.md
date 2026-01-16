Based on your requirements for a script that exits with an error code indicating the presence of the issue and exits with code 0 if the issue is resolved, I have adjusted the `reproducer.py` script accordingly. This time, I'm ensuring that the script logic is structured properly to catch the specific `AttributeError` and exit with code 1 when the issue is raised or 0 if no error occurs. The guidance on printing a stack trace has been incorporated correctly to provide detailed error information.

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

def check_date_accessor():
    import xarray as xr
    import pandas as pd
    time_coord = pd.date_range("2020-01-01", "2020-01-03", freq="12H")
    da = xr.DataArray([1, 2, 3, 4, 5], dims=["time"], coords={'time': time_coord})

    try:
        # Attempt to access the `.date` property
        date_output = da.time.dt.date
        print("No issue found, the `.date` accessor is working as expected.")
        return 0  # Exit with 0 if the issue is fixed
    except AttributeError as e:
        # Caught the AttributeError, indicating the `.date` accessor is not implemented
        print_stacktrace(e)
        return 1  # Exit with 1 to indicate failure due to the issue

if __name__ == "__main__":
    exit_code = check_date_accessor()
    exit(exit_code)
```

The script defines the `check_date_accessor` function, which attempts to access the `.date` attribute on the datetime accessor of an `xarray` DataArray. If the attribute access fails due to an `AttributeError`, it's caught, and the stack trace is printed using the provided `print_stacktrace` function. This behavior indicates that the issue is still present, thus forcing the script to exit with code 1. Conversely, if the `.date` attribute can be successfully accessed (indicating the issue has been resolved), the script will print a success message and exit with code 0.