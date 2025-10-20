# reproducer.py
def reproduce_issue():
    import xarray as xr

    # Define a function to print the stack trace
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

    TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
    valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
    invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
    ds = xr.merge([valid_times, invalid_times])

    try:
        xr.decode_cf(ds)
        # If no error is raised, assert to fail
        assert False, "Error expected but not raised"
    except Exception as e:
        print_stacktrace(e)
        error_msg = str(e)
        # Check if the error message includes the problematic variable's names
        # We're assuming the error message to ultimately include variable names once the issue is resolved
        if "invalid_times" in error_msg:
            print("Issue fixed. Error message now includes the problematic variable name.")
            exit(0)
        else:
            raise AssertionError("Issue present. Error message does not include the problematic variable name.")

if __name__ == "__main__":
    reproduce_issue()
