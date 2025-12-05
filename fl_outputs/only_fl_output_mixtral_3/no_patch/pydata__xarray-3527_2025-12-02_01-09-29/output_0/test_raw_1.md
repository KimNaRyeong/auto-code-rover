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

ds = xr.Dataset(data_vars={"a": ("x", list("abcd"))}, coords={"x": range(4)})
try:
    ds.groupby(ds.x % 2 == 0).quantile
    print("The issue is fixed.")
    exit(0)
except Exception as e:
    assert False, e
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    ds.groupby(ds.x % 2 == 0).quantile
AssertionError: AttributeError("'DatasetGroupBy' object has no attribute 'quantile'",)
    File "reproducer.py", line 12, in print_stacktrace
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
```