 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from astropy.table import Table
import astropy.units as u
from astropy.coordinates import SkyCoord

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    ras = [10, 20] * u.deg
    decs = [32, -2] * u.deg

    str_col = ['foo', 'bar']
    coords = SkyCoord(ra=ras, dec=decs)

    table = Table([str_col, coords], names=['col1', 'col2'])
    try:
        table.group_by('col1').groups.aggregate(np.mean)
    except Exception as e:
        print_stacktrace(e)
        assert False
```
This script should raise an `AssertionError` when executed with the specified environment, as described in the issue.