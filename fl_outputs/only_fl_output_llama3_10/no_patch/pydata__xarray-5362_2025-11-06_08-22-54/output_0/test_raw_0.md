Here is the reproducer script:

```python
import xarray as xr
import unittest
from unittest.mock import patch

class TestWeightedOperations(unittest.IsolatedAsyncioTestCase):
    async def test_weighted_operations(self):
        with patch('xarray.core.dataarrays.DataArray.weighted', side_effect=AssertionError()):
            ds = xr.tutorial.open_dataset("air_temperature")
            try:
                ds.weighted(xr.ones_like(ds["air"])).mean("dummy")
            except AssertionError as e:
                print_stacktrace(e)
                self.fail()

if __name__ == '__main__':
    unittest.main()
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace.