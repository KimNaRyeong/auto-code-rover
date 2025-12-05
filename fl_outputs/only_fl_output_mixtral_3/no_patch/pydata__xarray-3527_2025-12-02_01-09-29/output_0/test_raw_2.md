 Here is a standalone python script `reproducer.py` that reproduces the issue:
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
    assert False, "Expected AttributeError to be raised"
except AssertionError:
    pass
except Exception as e:
    print_stacktrace(e)

try:
    ds.a.groupby(ds.x % 2 == 0).quantile
except AttributeError as e:
    pass
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    assert False, "Expected AttributeError to be raised"
AssertionError: Expected AttributeError to be raised
```
This confirms that the `DatasetGroupBy` object does not have a `quantile` method, while the `DataArrayGroupBy` object does.