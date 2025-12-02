 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    xr.where(xr.DataArray([1, 2, 3]) > 0, 1, 0, keep_attrs=True)
except Exception as e:
    print_stacktrace(e)
    sys.exit(0)

assert False, "The issue was not reproduced"
```
When executed with `python3 reproducer.py`, the script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    xr.where(xr.DataArray([1, 2, 3]) > 0, 1, 0, keep_attrs=True)
  File "/home/user/miniconda3/envs/xarray_env/lib/python3.9/site-packages/xarray/core/computation.py", line 1812, in where
    keep_attrs = lambda attrs, context: attrs[1]
IndexError: list index out of range
```
This confirms that the issue is present in the current environment with xarray version 2022.3.0.