Here is the reproducer script:

```python
import xarray as xr
import numpy as np

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

def test_sum_min_count():
    da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
    try:
        da.sum(["dim_0", "dim_1"], min_count=2)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_sum_min_count()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script creates a standalone Python file that attempts to reproduce the issue. It defines a function `test_sum_min_count` that creates an xarray DataArray and tries to call the `sum` method with `min_count=2`. If the operation raises an AssertionError, it prints the stack trace and raises the exception again.