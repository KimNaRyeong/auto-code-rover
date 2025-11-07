```python
import xarray as xr
import numpy as np

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

def main():
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    try:
        # Check if the data types are the same
        assert ds['a'].values.dtype == ds.stack(b=('a',))['a'].values.dtype, "Data type changed after stack"
    except AssertionError as e:
        print_stacktrace(e)
        # Exit with code 1 to indicate an error
        exit(1)
    # If no error, print a success message and exit with code 0
    print("Success: Data type did not change after stack")
    exit(0)

if __name__ == "__main__":
    main()
```