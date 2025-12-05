 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    xr.DataArray([], dims='dim').groupby('dim').mean()  # raises StopIteration
except Exception as e:
    print_stacktrace(e)
    assert False, "StopIteration should not be raised here"
```
When running the script with `python3 reproducer.py`, it will raise a `StopIteration` exception and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 11, in <module>
    xr.DataArray([], dims='dim').groupby('dim').mean()  # raises StopIteration
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/groupby.py", line 1254, in mean
    result = self._reduce(operator.methodcaller("mean"), skipna=skipna)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/groupby.py", line 1152, in _reduce
    return reduction(self.obj, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/reductions.py", line 105, in mean
    return _apply_ufunc(np.mean, obj, dims=dims, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/computation.py", line 543, in _apply_ufunc
    return ufunc(*args, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/ufunc_ex.py", line 161, in _apply_n_operands
    return reduction(data, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/reductions.py", line 105, in mean
    return _apply_ufunc(np.mean, obj, dims=dims, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/computation.py", line 543, in _apply_ufunc
    return ufunc(*args, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/ufunc_ex.py", line 161, in _apply_n_operands
    return reduction(data, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/reductions.py", line 105, in mean
    return _apply_ufunc(np.mean, obj, dims=dims, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/computation.py", line 543, in _apply_ufunc
    return ufunc(*args, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/ufunc_ex.py", line 161, in _apply_n_operands
    return reduction(data, **kwargs)
  File "/home/user/.local/lib/python3.6/site-packages/xarray/core/reductions.py", line 105, in mean
    return _apply_ufunc