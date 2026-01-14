 Here is a revised standalone python file `reproducer.py` to reproduce the issue:

```python
import xarray as xr
import numpy as np

def standardize(x):
    return (x - x.mean()) / x.std()

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    ds = xr.Dataset()
    ds["variable"] = xr.DataArray(np.random.rand(4,3,5), {"lat":np.arange(4), "lon":np.arange(3), "time":np.arange(5)}, ("lat", "lon", "time"), )
    ds["id"] = xr.DataArray(np.arange(12.0).reshape((4,3)), {"lat": np.arange(4), "lon": np.arange(3)}, ("lat", "lon"), )
    ds["id"].values[0,0] = np.nan
    ds.groupby("id").apply(standardize)
except Exception as e:
    print_stacktrace(e)
    raise e
```

When running the script, it should raise an `IndexError` with the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    ds.groupby("id").apply(standardize)
  File "C:\Miniconda3\envs\main\lib\site-packages\xarray\core\groupby.py", line 609, in apply
    return self._combine(applied)
  File "C:\Miniconda3\envs\main\lib\site-packages\xarray\core\groupby.py", line 616, in _combine
    combined = concat(applied, dim)
  File "C:\Miniconda3\envs\main\lib\site-packages\xarray\core\concat.py", line 667, in concat
    return concat_dataarrays(data_arrays, dim, data_vars, coords, compat, **kwargs)
  File "C:\Miniconda3\envs\main\lib\site-packages\xarray\core\concat.py", line 588, in concat_dataarrays
    arrays = [_apply_dask(a, lazy) for a in arrays]
  File "C:\Miniconda3\envs\main\lib\site-packages\xarray\core\concat.py", line 588, in <listcomp>
    arrays = [_apply_dask(a, lazy) for a in arrays]
  File "C:\Miniconda3\envs\main\lib\site-packages\xarray\core\concat.py", line 574, in _apply_dask
    return dask.array.from_array(a, chunks=a.chunksize)
  File "C:\Miniconda3\envs\main\lib\site-packages\dask\array\core.py", line 1661, in from_array
    arrays = [_maybe_wrap(x, chunks) for x in arrays]
  File "C:\Miniconda3\envs\main\lib\site-packages\dask\array\core.py", line 1661, in <listcomp>
    arrays = [_maybe_wrap(x, chunks) for x in arrays]
  File "C:\Miniconda3\envs\main\lib\site-packages\dask\array\core.py", line 1649, in _maybe_wrap
    return _wrap_arraylike(x, chunks)
  File "C:\Minic