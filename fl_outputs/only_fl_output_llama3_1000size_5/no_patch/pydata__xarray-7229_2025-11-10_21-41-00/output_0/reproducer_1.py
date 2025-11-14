import xarray as xr
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

def reproduce_issue():
    ds = xr.tutorial.load_dataset("air_temperature")
    result = xr.where(True, ds.air, ds.air, keep_attrs=True).time.attrs
    if result != {'standard_name': 'time', 'long_name': 'Time'}:
        raise AssertionError("Coordinate attributes are not preserved")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced. All tests passed.")
exit(0)
