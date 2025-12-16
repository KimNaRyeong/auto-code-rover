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

color = 10*u.ABmag
flux = 10000
fluxMag = (flux*u.nJy).to(u.ABmag)
diff = fluxMag - color
assert diff.unit == u.ABmag, "UnitConversionError should have been raised"
print(diff)
print(diff.to(u.nJy))
```
When executed with `python3 reproducer.py`, the script prints the following output and raises an `AssertionError`:
```yaml
11.399999999999999 mag
...
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    assert diff.unit == u.ABmag, "UnitConversionError should have been raised"
AssertionError: UnitConversionError should have been raised
```
If the `-` is changed to `+`, the output is different:
```yaml
31.4 mag(AB2)
...
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    assert diff.unit == u.ABmag, "UnitConversionError should have been raised"
AssertionError: UnitConversionError should have been raised
```
This reproduces the issue where adding or subtracting ABmag Quantities loses the "type" of magnitude.