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

def main():
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()
    try:
        xr.decode_cf(ds)
        print('Issue is fixed.')
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError('Issue with scale_factor as length-1 list detected.') from None

if __name__ == "__main__":
    main()
```
This script checks for the issue where decoding CF fails when `scale_factor` and `add_offset` are encoded as length-1 lists in xarray. If the issue is present, it prints the stack trace using the given function and raises an `AssertionError`. If the issue is fixed, it simply prints that the issue is fixed.