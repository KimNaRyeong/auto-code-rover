import xarray as xr
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

def test_time_decoding_with_variable_name_in_error_message():
    TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
    valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
    invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
    ds = xr.merge([valid_times, invalid_times])
    
    try:
        xr.decode_cf(ds)
        # If the code reaches this point without raising an exception,
        # it means the issue is potentially fixed.
        print("The issue seems to be fixed.")
        sys.exit(0)
    except OverflowError as e:
        # Check if the error message is improved to include the variable name.
        # This is a placeholder for the future enhancement.
        # For now, we expect an error and the test is to ensure the stack trace is printed.
        print_stacktrace(e)
    except ValueError as e:
        print_stacktrace(e)
        # Fail the test if we catch a ValueError that does not contain variable name information.
        # This assertion is based on the expected behavior that in the future,
        # the error message includes the variable name causing the issue.
        assert "invalid_times" in str(e), "Error message does not contain the variable name."
    except Exception as e:
        # If any other exception occurs, print its stack trace.
        print_stacktrace(e)
        raise AssertionError("Unexpected error type encountered.")

if __name__ == "__main__":
    test_time_decoding_with_variable_name_in_error_message()
