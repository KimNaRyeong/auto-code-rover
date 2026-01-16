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

def test_deep_copy_behavior():
    import xarray as xr
    try:
        a = xr.DataArray(1.0, attrs={})
        b = xr.DataArray(2.0, attrs={})
        a.attrs["other"] = b
        b.attrs["other"] = a
        a.copy(deep=True)  # Attempt to make a deep copy
        print("Issue not present, deep copy succeeded without raising RecursionError.")
    except RecursionError as e:
        print_stacktrace(e)
        raise AssertionError("RecursionError occurred during deep copy.")

if __name__ == "__main__":
    test_deep_copy_behavior()
