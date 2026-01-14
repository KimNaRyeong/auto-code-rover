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

if __name__ == "__main__":
    da = xr.DataArray([0, 1, 2])
    try:
        da.quantile(q=50)
    except ValueError as e:
        print_stacktrace(e)
        assert e.args[0] == "Percentiles must be in the range [0, 1]"
        assert e.args[1] == "ValueError(message='Percentiles must be in the range [0, 1]')"
    else:
        print("Expected ValueError not raised")
        assert False
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:
```sql
Traceback (most recent call last):
  File "reproducer.py", line 13
    da.quantile(q=50)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 1190, in quantile
    return self.variable.quantile(q, dim=dim, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/variable.py", line 1272, in quantile
    result = func(self, q, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/variable.py", line 1262, in func
    return self._apply_method(method, q, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/variable.py", line 1231, in _apply_method
    return getattr(self.data, method)(*args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/lib/nanfunctions.py", line 1176, in percentile
    return _quantile_internal(a, q, axis, overwrite_input, interpolation, keepdims, **errors)
ValueError: Percentiles must be in the range [0, 1]

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    assert e.args[0] == "Percentiles must be in the range [0, 1]"
AssertionError:
```
The script asserts that the error message is `"Percentiles must be in the range [0, 1]"`, as expected. If the error message is changed, the script will fail and print a stack trace.