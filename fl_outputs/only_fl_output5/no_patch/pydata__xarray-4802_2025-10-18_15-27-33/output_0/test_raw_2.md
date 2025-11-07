Certainly, to create a standalone Python file named `reproducer.py` that aims to reproduce the reported issue with `xarray` where `decode_cf` fails when `scale_factor` is a length-1 list, and follows the given instructions for stack trace printing, you can use the following code:

```python
# reproducer.py
import xarray as xr

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

try:
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                            'add_offset': [1.0]}).to_dataset()
    xr.decode_cf(ds)
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("decode_cf fails when scale_factor is a length-1 list")
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("An unexpected error occurred")
else:
    print("No error encountered. The issue might be fixed.")
```

This script checks for the specific issue with decoding CF conventions in xarray when `scale_factor` and `add_offset` are provided as length-1 lists, and uses the provided function to print stack traces in case of exceptions, enabling clear identification of the issue within the library. The script should be placed in the root directory of the project and executed as `python3 reproducer.py` as per your direction.