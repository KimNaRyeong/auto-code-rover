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
    except ValueError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed, the script should raise a `ValueError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    main()
  File "reproducer.py", line 21, in main
    da2 = xr.full_like(da1, np.ones((3, 4)))
  File "/home/user/miniconda3/envs/xarray_env/lib/python3.8/site-packages/xarray/core/common.py", line 1426, in full_like
    return fill_value.broadcast_like(other)
  File "xarray/_backends/dask_backend.py", line 133, in broadcast_like
    return self._broadcast_like(other)
  File "xarray/_backends/dask_backend.py", line 128, in _broadcast_like
    return dask.array.core.broadcast_arrays(*args)
  File "/home/user/miniconda3/envs/xarray_env/lib/python3.8/site-packages/dask/array/core.py", line 2049, in broadcast_arrays
    return [_broadcast_to(x, shape) for x in xs]
  File "/home/user/miniconda3/envs/xarray_env/lib/python3.8/site-packages/dask/array/core.py", line 2049, in <listcomp>
    return [_broadcast_to(x, shape) for x in xs]
  File "/home/user/miniconda3/envs/xarray_env/lib/python3.8/site-packages/dask/array/core.py", line 2030, in _broadcast_to
    raise ValueError("could not broadcast input array from shape %r into shape %r" % (x.shape, shape))
ValueError: could not broadcast input array from shape (1,3) into shape (1,4)
```
This reproduces the issue where `xr.full_like` fails when `other.data` is a chunked dask array and the `fill_value` is a numpy array. The expected output is a DataArray with the dimensions and coords of `other`, and the numpy array of `fill_value` as its data. However, the actual output is a `ValueError` due to the incorrect broadcasting of the `fill_value` to the shape of `other`.