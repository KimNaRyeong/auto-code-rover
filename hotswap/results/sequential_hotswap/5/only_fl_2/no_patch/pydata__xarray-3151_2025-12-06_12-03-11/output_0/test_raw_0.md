 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

yCoord = ['a', 'c', 'b']  # raises ValueError on combine

ds1 = xr.Dataset(
    data_vars=dict(
        data=('x', 'y', np.random.rand(3, 3))
    ),
    coords=dict(
        x=(['x'], [1, 2, 3]),
        y=(['y'], yCoord)
    )
)

ds2 = xr.Dataset(
    data_vars=dict(
        data=('x', 'y', np.random.rand(4, 3))
    ),
    coords = dict(
        x=(['x'], [4, 5, 6, 7]),
        y=(['y'], yCoord)
    )
)

try:
    ds3 = xr.combine_by_coords((ds1, ds2))
except ValueError as e:
    print_stacktrace(e)
    assert False
except Exception as e:
    print_stacktrace(e)
    assert False
else:
    assert True
```
This script should raise a `ValueError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.