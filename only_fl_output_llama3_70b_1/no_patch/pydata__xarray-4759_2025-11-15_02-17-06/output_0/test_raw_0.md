Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import xarray as xr

def test_issue():
    da1 = xr.DataArray(data=np.arange(4).reshape([2, 2]),
                       dims=["x1", "x2"],
                       coords={"x1": np.array([0, 1]), 
                               "x2": np.array(['a', 'b'])})
    da2 = xr.DataArray(data=np.arange(4).reshape([2, 2]),
                       dims=["x1", "x2"],
                       coords={"x1": np.array([1, 2]), 
                               "x2": np.array(['c', 'd'])})

    da_joined = xr.concat([da1, da2], dim="x2")

    try:
        assert da_joined.coords["x2"].data.dtype.kind == 'U'
        print("Issue not present: dtype of DataArray coordinates stays the same.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == "__main__":
    test_issue()
```
This script will raise an `AssertionError` if the issue is present, and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.