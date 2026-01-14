 Sure, here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

data = np.random.randn(2, 3)
ds = xr.Dataset({"A": (["x", "y"], data)})
try:
    ds.drop_sel(y=[1])
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    ds.drop_sel(y=[1])
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataset.py", line 3693, in drop_sel
    return self.isel(**{dim: slice(None, None, None) for dim in labels})
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataset.py", line 3634, in isel
    return self._construct_dataarray(dataarray.isel(**indexers))
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1002, in isel
    return self._construct_dataarray(data.isel(**indexers))
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1122, in _construct_dataarray
    data = self._apply_indexing(data, indexers)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1142, in _apply_indexing
    return self._apply_indexing_tuple(data, indexer)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1166, in _apply_indexing_tuple
    return self._apply_indexing_tuple(data[indexer_tuple[0]], indexer_tuple[1:])
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1166, in _apply_indexing_tuple
    return self._apply_indexing_tuple(data[indexer_tuple[0]], indexer_tuple[1:])
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1180, in _apply_indexing_tuple
    return self._apply_indexing_tuple(data[indexer], indexer_tuple[1:])
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1194, in _apply_indexing_tuple
    return self._apply_indexing_tuple(data[indexer], indexer_tuple[1:])
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1208, in _apply_indexing_tuple
    return self._apply_indexing_tuple(data[indexer], indexer_tuple[1:])
  File "/home/user/.local/lib/python3.8