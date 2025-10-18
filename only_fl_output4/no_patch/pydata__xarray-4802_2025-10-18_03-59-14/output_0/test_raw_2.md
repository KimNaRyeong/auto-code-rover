Understood, let's reframe the task with a clear focus on directly addressing the exact issue regarding `decode_cf` with `scale_factor` being a length-1 list, as you've requested. The script will specifically check for an `AttributeError` associated with this bug and will use the provided function for printing the stack trace to comply with your guidelines.

Please find below the corrected standalone script `reproducer.py` designed to be executed in the root directory of your project:

```python
# reproducer.py
import xarray as xr
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
    sys.exit(0)  # Indicate success/no issue.
except AttributeError as e:
    # Print stack trace for the specific AttributeError
    print_stacktrace(e)
    sys.exit(1)  # Indicate failure/issue present.
```

Make sure you have the required environment and dependencies (like `xarray`) installed to run this script properly. The script attempts to reproduce the specified issue by creating a `DataArray` with `scale_factor` and `add_offset` as length-1 lists and then decoding it using `decode_cf`. If the issue exists, it will catch the `AttributeError`, print a detailed stack trace using the provided `print_stacktrace` function, and exit with code 1. Otherwise, it will announce the absence of the issue and exit with code 0.