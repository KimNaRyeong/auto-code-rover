Here is the reproducer script:

```python
import xarray as xr
import numpy as np

def test_issue():
    da1 = xr.DataArray(data=np.arange(4).reshape([2, 2]), 
                       dims=["x", "y"], 
                       coords={"x": np.array([0, 1]), 
                               "y": np.array(['a', 'b'])})
    
    da2 = xr.DataArray(data=np.arange(4).reshape([2, 2]), 
                       dims=["x", "y"], 
                       coords={"x": np.array([1, 2]), 
                               "y": np.array(['c', 'd'])})
    
    da_joined = xr.concat([da1, da2], dim="y")
    
    if da_joined.coords["y"].dtype != '<U1':
        raise AssertionError("Expected dtype to be <U1 but got {}".format(da_joined.coords["y"].dtype))
    
    print_stacktrace(Exception("Issue not present"))

test_issue()
```

This script creates two DataArrays, concatenates them along the "y" dimension, and checks if the dtype of the "y" coordinates is still '<U1'. If it's not, an AssertionError is raised with a stack trace.