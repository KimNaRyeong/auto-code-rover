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

This script creates a DataArray with `scale_factor` and `add_offset` attributes, both of which are length-1 lists. It then attempts to decode the dataset using `xr.decode_cf`. If an exception is raised, it prints the stack trace and raises an `AssertionError`, indicating that the issue should not be present.

Please note that you may need to adjust the script based on your specific environment and setup.