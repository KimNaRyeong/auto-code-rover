Here is the reproducer script:

```python
import xarray as xr
import numpy as np

def standardize(x):
    return (x - x.mean()) / x.std()

ds = xr.Dataset()
ds["variable"] = xr.DataArray(np.random.rand(4,3,5), 
                               {"lat":np.arange(4), "lon":np.arange(3), "time":np.arange(5)}, 
                               ("lat", "lon", "time"),
                              )

ds["id"] = xr.DataArray(np.arange(12.0).reshape((4,3)),
                         {"lat": np.arange(4), "lon":np.arange(3)},
                         ("lat", "lon"),
                        )

ds["id"].values[0,0] = np.nan

try:
    ds.groupby("id").apply(standardize)
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected IndexError"
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.