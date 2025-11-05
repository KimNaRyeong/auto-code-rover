Here is the reproducer script:

```python
import xarray as xr
import sys
from traceback import extract_tb, print_exception

def print_stacktrace(e: Exception):
    tb = extract_tb(e.__traceback__)
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
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("DatasetGroupBy does not implement quantile")
```

This script will reproduce the issue by attempting to call `quantile` on a grouped dataset. If the issue is present, it will print the stack trace and then raise an `AssertionError`.