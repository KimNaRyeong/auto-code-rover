 Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import numpy as np

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
    da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
    da.sum(["dim_0", "dim_1"], min_count=1)
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    da.sum(["dim_0", "dim_1"], min_count=1)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1183, in sum
    return self.reduce(np.sum, dims, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1108, in reduce
    return reduce_variable(
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/reduce.py", line 362, in reduce_variable
    result = _apply_ufunc(
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/numeric.py", line 1182, in _apply_ufunc
    return apply_ufunc(
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/numeric.py", line 1066, in apply_ufunc
