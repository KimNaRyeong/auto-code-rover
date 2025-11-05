Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from io import StringIO
import sys
import traceback

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

def reproduce_issue():
    try:
        ds = xr.DataArray([0, 1, 2], name='foo',
                          attrs={'scale_factor': [0.01],
                                 'add_offset': [1.0]}).to_dataset()
        xr.decode_cf(ds)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to create a dataset with `scale_factor` and `add_offset` encoded as length-1 lists, then try to decode it using `xr.decode_cf`. If the decoding fails (which it should), the script will print the stack trace of the error and exit with code 1.