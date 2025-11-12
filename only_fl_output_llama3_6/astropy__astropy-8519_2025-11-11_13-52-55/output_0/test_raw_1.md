Here is the reproducer script:

```python
import astropy.units as u
from astropy import units as uu

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
    color = 10*u.ABmag
    fluxMag = (10000*u.nJy).to(u.ABmag)
    diff1 = fluxMag - color
    diff2 = fluxMag + color

    print(color, fluxMag, diff1)
    print(diff1.to(u.nJy))
    print(diff2)

    assert diff1.unit == u.ABmag and diff2.unit == u.ABmag, "Issue: Adding/subtracting ABmag Quantities loses the 'type' of magnitude"

except Exception as e:
    print_stacktrace(e)
    raise
```

This script will reproduce the issue by performing both subtraction and addition operations on `ABmag` quantities. The assertion at the end checks if the resulting units are still `ABmag`, which should fail when the issue is present, printing a stack trace of the error.