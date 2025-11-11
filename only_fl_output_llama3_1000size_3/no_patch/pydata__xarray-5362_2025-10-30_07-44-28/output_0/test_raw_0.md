Here is the reproducer script:

```python
import xarray as xr
import unittest
from unittest.mock import patch

class TestWeightedOperations(unittest.IsolatedAsyncioTestCase):
    @patch('xarray.core.common._ensure_single_value')
    def test_weighted_operations(self, _ensure_single_value_mock):
        ds = xr.tutorial.open_dataset("air_temperature")
        with self.assertRaises(AssertionError):
            ds.weighted(xr.ones_like(ds["air"])).mean("dummy")

if __name__ == '__main__':
    unittest.main()
```

This script uses the `unittest` module to create a test case for the issue. The `test_weighted_operations` method mocks the `_ensure_single_value` function from xarray and then calls the weighted operation with a dummy dimension. If the issue is present, it should raise an `AssertionError`.