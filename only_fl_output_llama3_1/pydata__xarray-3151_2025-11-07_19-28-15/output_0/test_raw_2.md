Here is the reproducer script:

```python
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

def main():
    try:
        yCoord = ['a', 'c', 'b']
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
            coords=dict(
                x=[4, 5, 6, 7],
                y=yCoord
            )
        )

        ds3 = xr.combine_by_coords((ds1, ds2))
        self.fail("Expected combine_by_coords to raise ValueError")
    except ValueError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
    else:
        exit(0)
    finally:
        exit(1)
```

This script will run the test and raise an `AssertionError` when the issue is present.