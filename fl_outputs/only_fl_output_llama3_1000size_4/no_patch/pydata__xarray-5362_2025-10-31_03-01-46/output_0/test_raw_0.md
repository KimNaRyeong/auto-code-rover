Here is the reproducer script:

```python
import xarray as xr
import unittest
from unittest.mock import patch

class TestWeightedOperations(unittest.IsolatedAsyncioTestCase):
    async def test_weighted_operations(self):
        with self.assertRaises(AssertionError) as e:
            ds = xr.tutorial.open_dataset("air_temperature")
            ds.weighted(xr.ones_like(ds["air"])).mean("dummy")

        print_stacktrace(e.exception)

if __name__ == "__main__":
    unittest.main()
```

This script will run the test and if the issue is present, it will raise an `AssertionError` with a stack trace.