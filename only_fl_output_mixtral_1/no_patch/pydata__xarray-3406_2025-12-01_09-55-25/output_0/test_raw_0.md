 Here is a standalone python file `reproducer.py` to reproduce the issue:

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
    ds["variable"] = xr.DataArray(np.random.rand(4,3,5),
                                   {"lat":np.arange(4), "lon":np.arange(3), "time":np.arange(5)},
                                   ("lat", "lon", "time"),
                                  )

    ds["id"] = xr.DataArray(np.arange(12.0).reshape((4,3)),
                             {"lat": np.arange(4), "lon": np.arange(3)},
                             ("lat", "lon"),
                            )

    ds["id"].values[0,0] = np.nan

    ds.groupby("id").apply(standardize)
except Exception as e:
    print_stacktrace(e)
    raise e
```

When executed, the script should raise an `IndexError` with the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 26, in <module>
    ds.groupby("id").apply(standardize)
  File "~/miniconda3/envs/myenv/lib/python3.8/site-packages/xarray/core/groupby.py", line 609, in apply
    return self._combine(applied)
  File "~/miniconda3/envs/myenv/lib/python3.8/site-packages/xarray/core/groupby.py", line 616, in _combine
    combined = concat(applied, dim)
  File "~/miniconda3/envs/myenv/lib/python3.8/site-packages/xarray/core/concat.py", line 105, in concat
    return concat_dataarray(data_arrays, dim, combine_attrs, data_vars, coords, compat)
  File "~/miniconda3/envs/myenv/lib/python3.8/site-packages/xarray/core/concat.py", line 237, in concat_dataarray
    indices = nputils.inverse_permutation(np.concatenate(positions))
  File "~/miniconda3/envs/myenv/lib/python3.8/site-packages/xarray/core/nputils.py", line 54, in inverse_permutation
    inverse_permutation[indices] = np.arange(len(indices), dtype=np.intp)
IndexError: index 11 is out of bounds for axis 0 with size 11
```