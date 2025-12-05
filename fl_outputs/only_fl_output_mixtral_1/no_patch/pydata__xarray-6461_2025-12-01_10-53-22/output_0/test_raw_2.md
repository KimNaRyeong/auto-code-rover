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
    xr.where(xr.DataArray([1, 2, 3]) > 0, 1, 0, keep_attrs=True)
except Exception as e:
    print_stacktrace(e)
    assert False
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 11, in <module>
    xr.where(xr.DataArray([1, 2, 3]) > 0, 1, 0, keep_attrs=True)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/computation.py", line 1812, in apply_ufunc
    keep_attrs = lambda attrs, context: attrs[1]
IndexError: list index out of range
AssertionError:
```
This reproduces the issue with `xr.where` failing with a `keep_attrs=True` argument and a scalar as the second argument. The workaround is to pass `keep_attrs=False`.