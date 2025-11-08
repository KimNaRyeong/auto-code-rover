Here is the reproducer script:

```python
import xarray as xr
import numpy as np
import dask.array as da

def main():
    x = [1, 2, 3, 4]
    y = [1, 2, 3]
    da1 = xr.DataArray(da.ones((3, 4), chunks=(1, 4)), {"y": y, "x": x}, ("y", "x"))
    try:
        da2 = xr.full_like(da1, np.ones((3, 4)))
        print(da2.values)
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script creates a chunked dask array and then tries to create another DataArray using `xr.full_like` with the same shape but filled with ones. If an error occurs, it prints the stack trace.