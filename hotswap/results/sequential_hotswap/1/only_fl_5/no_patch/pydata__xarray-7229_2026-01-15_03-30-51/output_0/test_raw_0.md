```Python
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

def test_xr_where_keeps_coordinate_attrs():
    import xarray as xr
    try:
        ds = xr.tutorial.load_dataset("air_temperature")
        result_attrs = xr.where(True, ds.air, ds.air, keep_attrs=True).time.attrs
        expected_attrs = {'standard_name': 'time', 'long_name': 'Time'}
        if not all(item in result_attrs.items() for item in expected_attrs.items()):
            raise AssertionError("Coordinate attributes have been overwritten")
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with error status if the test fails.

if __name__ == "__main__":
    test_xr_where_keeps_coordinate_attrs()
    print("Test passed, no issue detected.")
    exit(0)  # Exit with success status if the test passes.
```