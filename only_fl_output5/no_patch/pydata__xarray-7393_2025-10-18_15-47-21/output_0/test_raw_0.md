```python
# reproducer.py
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
    try:
        ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
        assert ds['a'].values.dtype == ds.stack(b=('a',))['a'].values.dtype, \
            "dtype of coordinate 'a' changed after stacking"
    except AssertionError as e:
        print_stacktrace(e)
        print("\nIssue reproduced. Exiting with code 1.", file=sys.stderr)
        exit(1)
    else:
        print("Issue not reproduced. Exiting with code 0.")

if __name__ == "__main__":
    main()
```