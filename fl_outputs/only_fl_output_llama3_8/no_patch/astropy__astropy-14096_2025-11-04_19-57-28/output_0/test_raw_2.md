Here is the reproducer script:

```python
import astropy.coordinates as coord

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

try:
    class custom_coord(coord.SkyCoord):
        @property
        def prop(self):
            return self.random_attr

    c = custom_coord('00h42m30s', '+41d12m00s', frame='icrs')
    c.prop
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
else:
    assert False, "Expected AttributeError"
    exit(0)
```

This script defines the same subclass of `SkyCoord` and attempts to access a non-existent attribute. If the issue is present, it will print the stack trace and raise an `AssertionError`.