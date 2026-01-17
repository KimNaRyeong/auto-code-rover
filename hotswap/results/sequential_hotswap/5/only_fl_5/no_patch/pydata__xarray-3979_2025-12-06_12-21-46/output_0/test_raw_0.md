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

x = [1, 2, 3, 4]
y = [1, 2, 3]
da1 = xr.DataArray(da.ones((3, 4), chunks=(1, 4)), {"y": y, "x": x}, ("y", "x"))
try:
    da2 = xr.full_like(da1, np.ones((3, 4)))
    print(da2.values)
except Exception as e:
    print_stacktrace(e)
```
The script should raise a `ValueError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    da2 = xr.full_like(da1, np.ones((3, 4)))
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/common.py", line 1425, in full_like
    return fill_value.copy(data=dask.array.full(
  File "/home/user/.local/lib/python3.8/site-packages/dask/array/core.py", line 3515, in full
    chunks=chunks, 
  File "/home/user/.local/lib/python3.8/site-packages/dask/array/core.py", line 3541, in _full
    blocks = [full_block(shape, fill_value, chunks) for _ in range(num_blocks)]
  File "/home/user/.local/lib/python3.8/site-packages/dask/array/core.py", line 3541, in <listcomp>
    blocks = [full_block(shape, fill_value, chunks) for _ in range(num_blocks)]
  File "/home/user/.local/lib/python3.8/site-packages/dask/array/core.py", line 3535, in full_block
    return block.Block(shape, dtype, fill_value, chunks, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/dask/array/core.py", line 158, in __init__
    self.set_data(data)
  File "/home/user/.local/lib/python3.8/site-packages/dask/array/core.py", line 170, in set_data
    self._set_data(data)
  File "/home/user/.local/lib/python3.8/site-packages/dask/array/core.py", line 186, in _set_data
    self._update_shape_and_dtype(data)
  File "/home/user/.local/lib/python3.8/site-packages/dask/array/core.py", line 202, in _update_shape_and_dtype
    raise ValueError("could not broadcast input array from shape {} into shape {}".format(
ValueError: could not broadcast input array from shape (1,3) into shape (1,4)
```
The issue is that `xr.full_like` calls `dask.array.full` with the given number of chunks, which results in it trying to apply the `fill_value` for every individual chunk. This causes a `ValueError` when the `fill_value` is a numpy array with a different shape than the chunk.

The expected output is a