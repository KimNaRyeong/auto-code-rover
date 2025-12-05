 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from astropy.coordinates import Latitude

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

try:
    lat = np.float32(np.pi/2)
    Latitude(lat, 'rad')
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise a `ValueError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    Latitude(lat, 'rad')
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/astropy/coordinates/angles.py", line 564, in __new__
    self._validate_angles()
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/astropy/coordinates/angles.py", line 585, in _validate_angles
    raise ValueError('Latitude angle(s) must be within -90 deg <= angle <= 90 deg, '
ValueError: Latitude angle(s) must be within -90 deg <= angle <= 90 deg, got 90.00000250447816 deg
```
This reproduces the issue where the closest float32 value to pi/2 is slightly larger than pi/2, causing Astropy to reject it when checking with float64 precision.