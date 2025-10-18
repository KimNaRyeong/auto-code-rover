```python
import numpy as np
import xarray as xr

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

def test_drop_sel_without_coords():
    data = np.random.randn(2, 3)
    ds = xr.Dataset({"A": (["x", "y"], data)})
    try:
        ds.drop_sel(y=[1])
        raise AssertionError("drop_sel did not raise an error when expected")
    except ValueError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_drop_sel_without_coords()
```