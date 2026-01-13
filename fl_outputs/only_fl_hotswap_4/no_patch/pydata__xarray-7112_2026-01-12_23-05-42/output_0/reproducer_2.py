import xarray as xr
import copy
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    a = xr.DataArray(1.0, attrs={"other": None})
    b = xr.DataArray(2.0, attrs={"other": None})
    a.attrs["other"] = b
    b.attrs["other"] = a
    try:
        a_copy = a.copy(deep=True)
    except RecursionError as e:
        print_stacktrace(e)
        assert False, "RecursionError should not be raised"

if __name__ == "__main__":
    main()
