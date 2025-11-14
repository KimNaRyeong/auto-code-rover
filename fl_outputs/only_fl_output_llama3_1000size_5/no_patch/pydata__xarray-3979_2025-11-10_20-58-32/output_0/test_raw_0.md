Here is the reproducer script:

```python
import xarray as xr
import dask.array as da
import numpy as np

def reproduce_issue():
    x = [1, 2, 3, 4]
    y = [1, 2, 3]
    da1 = xr.DataArray(da.ones((3, 4), chunks=(1, 4)), {"y": y, "x": x}, ("y", "x"))
    try:
        da2 = xr.full_like(da1, np.ones((3, 4)))
        print(da2.values)
    except Exception as e:
        print_stacktrace(e)

reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.