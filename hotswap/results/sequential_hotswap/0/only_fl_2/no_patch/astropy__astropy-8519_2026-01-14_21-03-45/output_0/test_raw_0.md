```python
import numpy as np
import astropy.units as u
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

def main():
    try:
        # test subtraction
        color = 10*u.ABmag
        flux = 10000
        fluxMag = (flux*u.nJy).to(u.ABmag)
        diff = fluxMag - color

        assert diff.unit.is_equivalent(u.ABmag), "The result of subtraction should be an ABmag"

        # Uncomment to test addition - uncomment only after subtraction is fixed
        # sum_result = fluxMag + color
        # assert sum_result.unit.is_equivalent(u.ABmag), "The result of addition should be an ABmag"

        print(color, fluxMag, diff)
        print(diff.to(u.nJy))

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```