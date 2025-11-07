Here is the reproducer script:

```python
import xarray as xr
import numpy as np

def main():
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()
    try:
        xr.decode_cf(ds)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected decode_cf to fail")

if __name__ == '__main__':
    main()
```

This script creates a dataset with `scale_factor` and `add_offset` as length-1 lists, then attempts to decode it using `xr.decode_cf`. If the decoding fails (i.e., an exception is raised), the script prints the stack trace and raises an `AssertionError`.

Please note that you need to have xarray installed in your Python environment.