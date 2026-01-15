```python
# reproducer.py
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

def reproduce_subtraction_issue():
    # color = np.random.random(5)*u.ABmag
    color = 10*u.ABmag
    flux = 10000
    fluxMag = (flux*u.nJy).to(u.ABmag)
    try:
        diff = fluxMag - color
        print(color, fluxMag, diff)
        result = diff.to(u.nJy)
        print(result)
    except u.UnitConversionError as e:
        print_stacktrace(e)
        raise AssertionError("Unit conversion error encountered during subtraction")

def reproduce_addition_issue():
    color = 10*u.ABmag
    flux = 10000
    fluxMag = (flux*u.nJy).to(u.ABmag)
    try:
        sum_result = fluxMag + color
        print(color, fluxMag, sum_result)
        result = sum_result.to(u.nJy)
        print(result)
    except u.UnitConversionError as e:
        print_stacktrace(e)
        raise AssertionError("Unit conversion error encountered during addition")

if __name__ == "__main__":
    reproduce_subtraction_issue()
    reproduce_addition_issue()
```