Here is the `reproducer.py` file that reproduces the issue:
```
import astropy.coordinates as coord
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

try:
    class custom_coord(coord.SkyCoord):
        @property
        def prop(self):
            return self.random_attr

    c = custom_coord('00h42m30s', '+41d12m00s', frame='icrs')
    c.prop
except AttributeError as e:
    if str(e) != "'custom_coord' object has no attribute 'random_attr'":
        print_stacktrace(e)
        assert False, "Expected AttributeError with message 'custom_coord' object has no attribute 'random_attr'"
    else:
        sys.exit(1)
else:
    sys.exit(0)
```
This script should reproduce the issue and exit with code 1 when the issue is present. If the issue is fixed, it will exit with code 0.

Please note that this script assumes that `astropy` is installed and available in the Python environment where the script is executed.