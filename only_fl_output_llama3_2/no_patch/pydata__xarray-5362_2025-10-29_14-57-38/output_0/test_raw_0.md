Here is the reproducer script:

```python
import xarray as xr
import unittest
from unittest.mock import patch

class TestWeightedOperations(unittest.TestCase):

    @patch('xarray.core.groupby._get_groupby_obj')
    def test_weighted_operations(self, mock_get_groupby_obj):
        ds = xr.tutorial.open_dataset("air_temperature")
        with self.assertRaises(AssertionError):
            ds.weighted(xr.ones_like(ds["air"])).mean("dummy")

if __name__ == '__main__':
    unittest.main()
```

This script will run the test case and if the issue is present, it will raise an `AssertionError` and print a stack trace.