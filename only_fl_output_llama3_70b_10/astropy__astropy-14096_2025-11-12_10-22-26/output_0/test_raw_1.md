Here is the `reproducer.py` file to reproduce the issue:
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
    if str(e).startswith("'custom_coord' object has no attribute 'prop'"):
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate the issue is present
    else:
        raise  # Raise the exception if it's not the expected error
else:
    assert False, "Expected AttributeError"
    sys.exit(0)  # Exit with code 0 to indicate the issue is fixed