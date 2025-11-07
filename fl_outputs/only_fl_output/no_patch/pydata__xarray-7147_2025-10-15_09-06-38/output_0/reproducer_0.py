# reproducer.py
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
    import xarray as xr

    # Setup: creating a Dataset with valid and invalid time variables
    TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
    valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
    invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
    ds = xr.merge([valid_times, invalid_times])

    try:
        # Attempting to decode time variables
        xr.decode_cf(ds)
    except Exception as e:
        print_stacktrace(e)
        # Check that the error message includes the problematic variable's name
        assert "invalid_times" in str(e), "The error message does not include the problematic variable's name."
        return  # Exit function here if assertion passes
    
    # If the above assertion did not raise, it means the issue is fixed
    print("Issue fixed.")

if __name__ == "__main__":
    main()
