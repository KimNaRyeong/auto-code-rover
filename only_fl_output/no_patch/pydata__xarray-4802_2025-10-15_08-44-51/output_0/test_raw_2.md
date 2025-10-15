Given the details you've provided, here is how you can create a standalone Python file named `reproducer.py` to reproduce the issue outlined. This script checks if `xr.decode_cf()` can properly handle `scale_factor` and `add_offset` being encoded as length-1 lists. The script will raise an `AssertionError` if the issue persists, indicating the failure to handle such cases appropriately; otherwise, it will exit with code 0, signifying the issue has been resolved.

```python
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
    import xarray as xr

    # Create a DataArray with scale_factor and add_offset encoded as length-1 lists
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()

    # Attempt to apply scale and offset according to CF conventions
    decoded_ds = xr.decode_cf(ds)

    # If the code reaches this line without error, the issue is considered fixed
    print("The issue has been fixed.")
    sys.exit(0)

except AttributeError as e:
    # This block catches the specific error described in the issue and prints a stack trace
    print_stacktrace(e)
    raise AssertionError("Failed due to AttributeError as described in the issue.")

except Exception as e:
    # This block catches any other unexpected errors, prints a stack trace, and exits with error code
    print_stacktrace(e)
    sys.exit(1)
```

To use this script:
1. Save it as `reproducer.py` in the root directory of your project.
2. Execute the script using Python 3 by running the command `python3 reproducer.py` in your terminal.

The script is designed to specifically target the issue with encoding of `scale_factor` and `add_offset` as length-1 lists in xarray's `decode_cf` function, as described. Make sure you have xarray installed in your environment to test this successfully.