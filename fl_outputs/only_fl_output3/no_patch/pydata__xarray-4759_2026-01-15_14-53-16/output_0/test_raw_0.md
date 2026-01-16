```python
import numpy as np
import xarray as xr
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_dataset_coord_dtype_not_change():
    test = xr.Dataset(coords={'xy': ['x', 'y']})
    dtype_before = test['xy'].dtype

    test['test'] = xr.DataArray(np.array([0, 0]), dims=['xy'])
    dtype_after = test['xy'].dtype

    try:
        assert dtype_before == dtype_after, f"Expected dtype {dtype_before} but got {dtype_after}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with an error code to indicate the issue is present

def test_concat_coord_dtype_not_change():
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
        assert da1.coords["x1"].dtype == da_joined.coords["x1"].dtype, \
            f"coord x1 dtype changed after concat from {da1.coords['x1'].dtype} to {da_joined.coords['x1'].dtype}"
        assert da1.coords["x2"].dtype == da_joined.coords["x2"].dtype, \
            f"coord x2 dtype changed after concat from {da1.coords['x2'].dtype} to {da_joined.coords['x2'].dtype}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with an error code to indicate the issue is present

if __name__ == "__main__":
    test_dataset_coord_dtype_not_change()
    test_concat_coord_dtype_not_change()
    print("All tests passed successfully!")
    exit(0)  # Exit with code 0 to indicate the issue is fixed
```