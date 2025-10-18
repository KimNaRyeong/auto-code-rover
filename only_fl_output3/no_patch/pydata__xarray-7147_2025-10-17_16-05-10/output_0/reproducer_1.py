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

def reproduce_issue():
    import xarray as xr

    # Define time attributes according to the issue description
    TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
    
    # Create valid and invalid DataArrays
    valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
    invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
    
    # Merge them into a single Dataset
    ds = xr.merge([valid_times, invalid_times])
    
    try:
        # Attempt to decode the Dataset
        xr.decode_cf(ds)
        # If failure to decode does not occur, the issue might have been inadvertently resolved
        print("No exception was raised, which may indicate the issue has been resolved.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)

        # Checking if the error message contains any indication of the problematic variable
        error_message = str(e)
        if "invalid_times" not in error_message:
            # The issue is present if there's no mention of the problematic variable
            raise AssertionError("The error message does not identify the problematic variable.")
        else:
            # If the variable name is found, it means the issue might have been fixed
            print("The issue appears to have been addressed.")
            exit(0)

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        # An AssertionError indicates the test successfully found the issue
        print_stacktrace(e)
        exit(1)  # Exit with an error state if the issue is confirmed
    except Exception as e:
        # Any other exceptions are printed but we assume the issue exists
        print_stacktrace(e)
        exit(1)  # Exit with an error state if unexpected exceptions occur
    exit(0)  # An exit code of 0 indicates no issue found or it has been fixed
