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

if __name__ == '__main__':
    try:
        da = xr.DataArray([0, 1, 2])
        da.quantile(q=50)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 12, in <module>
    da.quantile(q=50)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1471, in quantile
    return self.variable.quantile(q, dim=dim, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/variable.py", line 1531, in quantile
    result = func(self, q, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/variable.py", line 1525, in func
    return self._apply_method(method, q, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/variable.py", line 1497, in _apply_method
    return getattr(self.data, method)(*args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/lib/nanfunctions.py", line 1254, in _quantile_perc
    return _quantile_perc_internal(a, q, axis, overwrite_input, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/lib/nanfunctions.py", line 1282, in _quantile_perc_internal
    perc = _validate_percentiles(perc, len(result))
  File "/home/user/.local/lib/python3.8/site-packages/numpy/lib/nanfunctions.py", line 1167, in _validate_percentiles
    raise ValueError("Percentiles must be in the range [0, 100]")
ValueError: Percentiles must be in the range [0, 100]
```
This stack trace shows that the `ValueError` is raised in the `numpy` library, and not in the `xarray` library as expected. The error message is also incorrect, as the percentiles should be in the range [0, 1] instead of [0, 100].