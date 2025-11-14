Here is the reproducer script:

```python
import xarray as xr
import unittest
from unittest.mock import patch

class TestDataArrayEquality(unittest.TestCase):

    def test_data_array_equality(self):
        da_withunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
        da_withunits.frequency.attrs["units"] = "GHz"
        print(da_withunits.frequency.units)

        da_withoutunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})

        with self.assertRaises(AssertionError):
            result = da_withunits == da_withoutunits
            print(result)
            print(da_withunits.frequency.units)

    def test_data_array_equality_after_comparison(self):
        da_withunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
        da_withunits.frequency.attrs["units"] = "GHz"
        print(da_withunits.frequency.units)

        da_withoutunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})

        result = da_withunits == da_withoutunits
        self.assertTrue(result)
        with self.assertRaises(AttributeError):
            print(da_withunits.frequency.units)

if __name__ == '__main__':
    unittest.main()
```

This script will run two tests. The first test checks if the comparison of two DataArrays raises an `AssertionError` when one DataArray has attributes that the other does not. The second test checks if the comparison still works correctly after the comparison operation, but then trying to access the attribute of the original DataArray raises an `AttributeError`.