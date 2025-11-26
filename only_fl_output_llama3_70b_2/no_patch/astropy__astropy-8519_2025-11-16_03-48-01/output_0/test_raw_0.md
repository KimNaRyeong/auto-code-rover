Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import numpy as np
import astropy.units as u

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
    flux = 10000
    fluxMag = (flux*u.nJy).to(u.ABmag)
    diff = fluxMag - color
    print(color, fluxMag, diff)
    assert diff.unit == u.ABmag, "Unit of difference is not ABmag"
    print(diff.to(u.nJy))
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
```
This script will reproduce the issue and raise an `AssertionError` when the unit of the difference is not `ABmag`. It will also print a stack trace of the exception. If the issue is fixed, the script will exit with code 0.