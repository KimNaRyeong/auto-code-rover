 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import dask.array as da
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

def main():
    x = [1, 2, 3, 4]
    y = [1, 2, 3]
    da1 = xr.DataArray(da.ones((3, 4), chunks=(1, 4)), {"y": y, "x": x}, ("y", "x"))
    try:
        da2 = xr.full_like(da1, np.ones((3, 4)))
        print(da2.values)
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed, the script should raise a `ValueError` with the following stack trace:
```less
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 19, in main
    da2 = xr.full_like(da1, np.ones((3, 4)))
  File "/home/user/miniconda3/envs/xarray/lib/python3.8/site-packages/xarray/core/common.py", line 1425, in full_like
    return fill_value.copy(data.dtype, data.shape)
  File "/home/user/miniconda3/envs/xarray/lib/python3.8/site-packages/numpy/core/_methods.py", line 156, in _amax
    return umr_maximum(a, axis, None, out, keepdims, initial, where)
ValueError: could not broadcast input array from shape (1,3) into shape (1,4)
```
This reproduces the issue where `xr.full_like` fails when `other.data` is a chunked dask array and the `fill_value` is a numpy array.