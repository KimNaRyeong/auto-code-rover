```python
# reproducer.py

import xarray as xr
import numpy as np


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


def reproduce_issue():
    #yCoord = ['a', 'b', 'c']  # works without error
    yCoord = ['a', 'c', 'b']  # raises ValueError on combine
    
    ds1 = xr.Dataset(
        data_vars=dict(
            data=(['x', 'y'], np.random.rand(3, 3))
        ),
        coords=dict(
            x=[1, 2, 3],
            y=yCoord
        )
    )
    
    ds2 = xr.Dataset(
        data_vars=dict(
            data=(['x', 'y'], np.random.rand(4, 3))
        ),
        coords = dict(
            x=[4, 5, 6, 7],
            y=yCoord
        )
    )
    
    try:
        ds3 = xr.combine_by_coords((ds1, ds2))
        print("combine_by_coords completed successfully.")
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("combine_by_coords raised a ValueError as expected due to non-monotonic identical coordinates.") from None

if __name__ == "__main__":
    reproduce_issue()
```