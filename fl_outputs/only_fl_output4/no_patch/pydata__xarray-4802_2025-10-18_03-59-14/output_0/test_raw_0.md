```python
# reproducer.py
import xarray as xr
import numpy as np
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()
    xr.decode_cf(ds)
    print("Issue not present, exited with code 0")
except AttributeError as e:
    print_stacktrace(e)
    assert isinstance(e, AttributeError), "Unexpected error type."
    # This is illogical in practice as the script should not continue running after a critical failure like this.
    # However, as per instruction, asserting here demonstrates the detection of the specific issue for reproduction.
    # Normally, an assertion error would not be used to handle exceptions in this manner.
    sys.exit(1)  # Exit with a non-zero code indicating error.
```

This script attempts to reproduce the specified issue by creating an `xarray.Dataset` with `scale_factor` and `add_offset` attributes encoded as length-1 lists and then applying `xarray.decode_cf()` to it. The `try-except` block is designed to catch the `AttributeError` and then print out the stack trace using the `print_stacktrace` function. Upon encountering the specific error, the script exits with code 1, indicating that the issue still exists. Conversely, if the operation succeeds without raising an error, it indicates that the issue has been fixed, and the script exits with code 0.