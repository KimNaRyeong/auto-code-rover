Based on the provided information, it seems that the issue is not related to the weighted operations in xarray but rather a warning and an error message from other parts of the code. The warning message is about the `pkg_resources` package being deprecated and slated for removal, and the error message is about the removal of `np.unicode_` in NumPy 2.0.

Here's a revised reproducer script that does not attempt to reproduce the issue with weighted operations:

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
    ds = xr.tutorial.open_dataset("air_temperature")
    ds.weighted(xr.ones_like(ds["air"])).mean("dummy")
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected error not raised"

if __name__ == "__main__":
    test_weighted_operations()
```

This script will attempt to open the air temperature dataset and perform a weighted operation. If an exception is raised, it will print the stack trace and fail the test.