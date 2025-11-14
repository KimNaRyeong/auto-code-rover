Here is the reproducer script:

```python
import xarray as xr
import traceback
import sys

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
    ds.a.groupby(ds.x % 2 == 0).quantile
    ds.groupby(ds.x % 2 == 0).quantile
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")

print("Issue not present")
exit(0)
```

This script will reproduce the issue by calling `ds.a.groupby(ds.x % 2 == 0).quantile` and then `ds.groupby(ds.x % 2 == 0).quantile`. If the issue is still present, it will print a stack trace of the error and raise an AssertionError.