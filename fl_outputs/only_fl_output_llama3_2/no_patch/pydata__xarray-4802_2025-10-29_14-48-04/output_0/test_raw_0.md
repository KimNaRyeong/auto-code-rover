Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from io import StringIO

def main():
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()
    try:
        xr.decode_cf(ds)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue should not be present")

if __name__ == "__main__":
    main()
```

This script creates a DataArray with `scale_factor` and `add_offset` attributes, both of which are length-1 lists. It then attempts to decode the dataset using `xr.decode_cf`. If an exception is raised, it prints the stack trace and raises an `AssertionError`, indicating that the issue should not be present.