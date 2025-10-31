Here is the reproducer script:

```python
import xarray as xr
import sys
import traceback

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
    ds.groupby(ds.x % 2 == 0).quantile
    ds.groupby(ds.x % 2 == 0).quantile.quantile(q=0.5)
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
else:
    print("Issue fixed, exiting with code 0")
    sys.exit(0)
```

This script will run the code that reproduces the issue and then check if the issue is present. If the issue is present, it will print the stack trace and raise an `AssertionError`.