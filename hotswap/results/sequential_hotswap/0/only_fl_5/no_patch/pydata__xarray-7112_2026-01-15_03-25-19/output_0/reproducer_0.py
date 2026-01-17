# reproducer.py
import xarray as xr

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
        a = xr.DataArray(1.0, attrs={})
        b = xr.DataArray(2.0, attrs={})

        # Create circular reference
        a.attrs["other"] = b
        b.attrs["other"] = a

        # Attempt to create a deep copy (should raise RecursionError)
        a_copy = a.copy(deep=True)

    except RecursionError as e:
        print_stacktrace(e)
        raise AssertionError("Issue with maximum recursion depth exceeded detected") from e
    else:
        print("No issues detected. Deep copy successful without exceeding maximum recursion depth.")

if __name__ == "__main__":
    main()
