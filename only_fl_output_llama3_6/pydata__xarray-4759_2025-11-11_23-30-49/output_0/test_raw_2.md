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

def reproduce_issue():
    try:
        test = xr.Dataset(coords={'xy': ['x', 'y']})
        test['test'] = xr.DataArray(np.array([0, 0]), dims=['xy'])
        da1 = xr.DataArray(data=np.arange(4).reshape([2, 2]), 
                            dims=["x1", "x2"], 
                            coords={"x1": np.array([0, 1]), 
                                    "x2": np.array(['a', 'b'])})
        da2 = xr.DataArray(data=np.arange(4).reshape([2, 2]), 
                            dims=["x1", "x2"], 
                            coords={"x1": np.array([1, 2]), 
                                    "x2": np.array(['c', 'd'])})
        da_joined = xr.concat([da1, da2], dim="x2")
        assert da_joined.coords["x1"].dtype == '<U1'
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script creates two data arrays and then concatenates them. It checks if the dtype of the 'x1' coordinate is still '<U1' after concatenation, and raises an AssertionError if it's not.