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
        raise AssertionError("Issue should not be present")

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

Please note that the script should be executed in an environment where xarray 0.16.2 or later is installed, and numpy 1.20.0 or earlier is installed.

Also, please ensure that you have the correct version of `h5netcdf` engine installed, as mentioned in your issue description.