Here is the reproducer script:

```python
import xarray as xr
import numpy as np
import unittest

class TestDatasetCoordinates(unittest.TestCase):

    def test_dataset_coordinates(self):
        # Create two DataArrays with different coordinates
        da1 = xr.DataArray(data=np.arange(4).reshape([2, 2]), 
                            dims=["x", "y"], 
                            coords={"x": np.array([0, 1]), 
                                   "y": np.array(['a', 'b'])})
        
        da2 = xr.DataArray(data=np.arange(4).reshape([2, 2]), 
                            dims=["x", "y"], 
                            coords={"x": np.array([1, 2]), 
                                   "y": np.array(['c', 'd'])})

        # Concatenate the DataArrays
        da_joined = xr.concat([da1, da2], dim="y")

        # Check if the dtype of coordinates has changed
        self.assertEqual(da1.coords["x"].dtype, da_joined.coords["x"].dtype)
        self.assertEqual(da1.coords["y"].dtype, da_joined.coords["y"].dtype)

    def test_dataset_coordinates_object_dtype(self):
        # Create two DataArrays with different coordinates and object dtype
        da1 = xr.DataArray(data=np.arange(4).reshape([2, 2]), 
                            dims=["x", "y"], 
                            coords={"x": np.array([b'\x00', b'\x01']), 
                                   "y": np.array(['a', 'b'])})

        da2 = xr.DataArray(data=np.arange(4).reshape([2, 2]), 
                            dims=["x", "y"], 
                            coords={"x": np.array([b'\x01', b'\x02']), 
                                   "y": np.array(['c', 'd'])})

        # Concatenate the DataArrays
        da_joined = xr.concat([da1, da2], dim="y")

        # Check if the dtype of coordinates has changed
        self.assertEqual(da1.coords["x"].dtype, da_joined.coords["x"].dtype)
        self.assertEqual(da1.coords["y"].dtype, da_joined.coords["y"].dtype)

if __name__ == '__main__':
    unittest.main()
```

This script contains two test cases. The first one tests the issue with integer dtype and the second one tests the issue with object dtype.