```python
# reproducer.py
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

def main():
    x1 = xr.Dataset(
        {
            "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
        },
        coords={"y": [0, 1], "x": [10, 20, 30]},
    )
    x2 = xr.Dataset(
        {
            "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
        },
        coords={"y": [2, 3], "x": [10, 20, 30]},
    )
    x3 = xr.Dataset(
        {
            "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
        },
        coords={"y": [2, 3], "x": [40, 50, 60]},
    )
    
    try:
        result = xr.combine_by_coords([x1, x2, x3])
        expected_dims = ['x', 'y']
        assert set(result.dims) == set(expected_dims), f"Dimensions mismatch. Expected {expected_dims}, got {list(result.dims)}"
        assert 'temperature' in result, "temperature variable is not in the result"
        assert result['temperature'].shape == (4, 6), f"Unexpected shape for 'temperature'. Expected (4, 6), got {result['temperature'].shape}"
        print("Issue is fixed.")
    except AssertionError as ae:
        print(ae)
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```