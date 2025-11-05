The issue is not reproduced because the script does not actually call `quantile` on a grouped dataset. The error message you see is due to an unrelated issue with numpy.

To reproduce the original issue, we need to create a dataset and group it by some variable, then try to call `quantile` on that grouped dataset. Here's how you can do it:

```python
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    ds = xr.Dataset(data_vars={"a": ("x", list("abcd"))}, coords={"x": range(4)})
    ds.groupby(ds.x % 2 == 0).quantile()
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
```

This script creates a dataset with two variables, then groups the data by whether the value of `x` is even or odd. It then tries to call `quantile` on that grouped dataset. If the issue is present, it will print a stack trace and exit with code 1.

However, this test did not reproduce the original issue because the error message you see is due to an unrelated issue with numpy.