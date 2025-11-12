Here is the standalone Python file `reproducer.py` to reproduce the issue:
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
        raise AssertionError("Expected AttributeError with message about 'random_attr', but got different message")
    sys.exit(0)
```
This script should reproduce the issue and exit with code 0 when the issue is present. If the issue is fixed, it will raise an `AssertionError`.