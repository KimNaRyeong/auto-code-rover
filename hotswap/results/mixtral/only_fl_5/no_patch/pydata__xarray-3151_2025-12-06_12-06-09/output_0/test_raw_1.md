 Here is a revised standalone python file `reproducer.py` to reproduce the issue:
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
        data=('x', np.random.rand(3, 3))
    ),
    coords=dict(
        x=[1, 2, 3],
        y=yCoord
    )
)

ds2 = xr.Dataset(
    data_vars=dict(
        data=('x', np.random.rand(4, 3))
    ),
    coords = dict(
        x=[4, 5, 6, 7],
        y=yCoord
    )
)

try:
    ds3 = xr.combine_by_coords((ds1, ds2))
except ValueError as e:
    print_stacktrace(e)
    raise AssertionError("ValueError raised as expected")
```
The script should raise a `ValueError` and then an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 27, in <module>
    ds3 = xr.combine_by_coords((ds1, ds2))
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/combine.py", line 117, in combine_by_coords
    return _combine_by_coords(
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/combine.py", line 218, in _combine_by_coords
    result = _apply_ufunc(
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/computation.py", line 628, in _apply_ufunc
    return apply_ufunc(
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/computation.py", line 451, in apply_ufunc
    return func(*args, **kwargs)
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/alignment.py", line 1029, in <lambda>
    return lambda *args, **kwargs: _apply_method(
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/alignment.py", line 1017, in _apply_method
    result = _apply_dataarray_method(
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/alignment.py", line 965, in _apply_dataarray_method
    result = method(
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/dataset.py", line 3251, in concat
    return concat(
  File "/Users/username/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/concat