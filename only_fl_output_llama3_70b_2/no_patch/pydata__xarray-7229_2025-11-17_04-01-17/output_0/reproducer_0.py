import xarray as xr
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    ds = xr.tutorial.load_dataset("air_temperature")
    result = xr.where(True, ds.air, ds.air, keep_attrs=True).time.attrs
    expected_attrs = {'standard_name': 'time', 'long_name': 'Time'}
    assert result == expected_attrs, "Coordinate attributes are not preserved"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
