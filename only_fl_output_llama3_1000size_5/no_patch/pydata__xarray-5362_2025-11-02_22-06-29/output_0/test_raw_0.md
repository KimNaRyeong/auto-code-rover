Here is the reproducer script:

```python
import xarray as xr
import pytest

def test_weighted_operations():
    ds = xr.tutorial.open_dataset("air_temperature")
    try:
        ds.weighted(xr.ones_like(ds["air"])).mean("dummy")
    except Exception as e:
        print_stacktrace(e)
        pytest.fail("Expected error not raised")

if __name__ == "__main__":
    test_weighted_operations()
```

This script will run the weighted operation and check if an exception is raised. If no exception is raised, it will print a stack trace of the issue and fail the test.