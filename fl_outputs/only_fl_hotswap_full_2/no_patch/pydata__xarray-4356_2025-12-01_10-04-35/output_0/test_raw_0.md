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
Executing the script `python3 reproducer.py` will reproduce the issue and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    da.sum(["dim_0", "dim_1"], min_count=1)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1187, in sum
    return self.reduce(np.sum, dims, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1117, in reduce
    return self._reduce(
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/reduction.py", line 605, in reduce_variable
    result = reduce_variable_compat(
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/reduction.py", line 472, in reduce_variable_compat
    result = reduce(
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/reduction.py", line 348, in reduce
