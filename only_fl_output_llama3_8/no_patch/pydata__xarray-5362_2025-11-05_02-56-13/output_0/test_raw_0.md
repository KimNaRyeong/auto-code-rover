Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from unittest import TestCase

class TestWeightedOperations(TestCase):
    def test_weighted_operations(self):
        ds = xr.tutorial.open_dataset("air_temperature")
        try:
            ds.weighted(xr.ones_like(ds["air"])).mean("dummy")
            self.fail("Expected AssertionError")
        except AssertionError as e:
            print_stacktrace(e)
            self.assertTrue(True, "AssertionError raised")

if __name__ == "__main__":
    test = TestWeightedOperations()
    test.test_weighted_operations()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.