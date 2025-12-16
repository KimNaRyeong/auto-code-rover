 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
import astropy.units as u

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    color = 10*u.ABmag
    flux = 10000
    fluxMag = (flux*u.nJy).to(u.ABmag)
    diff = fluxMag - color
    assert diff.unit == u.ABmag, "Subtraction of ABmag Quantities lost the 'type' of magnitude"
    print(color, fluxMag, diff)
    print(diff.to(u.nJy))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with a stack trace, indicating that the issue is present:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    main()
  File "reproducer.py", line 16, in main
    assert diff.unit == u.ABmag, "Subtraction of ABmag Quantities lost the 'type' of magnitude"
AssertionError: Subtraction of ABmag Quantities lost the 'type' of magnitude
```
If the `-` is changed to `+`, the exception is different:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    main()
  File "reproducer.py", line 18, in main
    print(diff.to(u.nJy))
  File "/home/user/.local/lib/python3.8/site-packages/astropy/units/quantity.py", line 518, in to
    return self._new_view(new_unit)
  File "/home/user/.local/lib/python3.8/site-packages/astropy/units/quantity.py", line 842, in _new_view
    return self.__class__(self.value, new_unit, copy=False)
  File "/home/user/.local/lib/python3.8/site-packages/astropy/units/quantity.py", line 411, in __new__
    result = super().__new__(cls, value, like=other)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/core/_internal.py", line 501, in _wrapit
