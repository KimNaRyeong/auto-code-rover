 Here is a standalone python script `reproducer.py` to reproduce the issue:

```python
import numpy as np
import xarray as xr
from reproducer import print_stacktrace

def main():
    data = np.random.rand(100)
    data[25] = np.nan
    da = xr.DataArray(data)

    # unchunked 