Below is the standalone Python file named `reproducer.py` that reflects your requirements. This script is intended to reproduce the issue described, print a detailed stack trace if the issue occurs, and exit normally if the issue is resolved.

```python
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


def test_inplace_addition():
    import numpy as np
    import xarray as xr

    n = 5

    d1 = np.arange(n)
    np.random.shuffle(d1)
    A = xr.DataArray(np.ones(n), coords=[('dim', d1)])

    d2 = np.arange(n)
    np.random.shuffle(d2)
    B = xr.DataArray(np.ones(n), coords=[('dim', d2)])

    try:
        # Expected that this operation will succeed
        A += B
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("In-place addition failed when it should succeed.")

    print("Test passed, in-place addition succeeded.")


if __name__ == "__main__":
    try:
        test_inplace_addition()
    except AssertionError as e:
        # Exit with code 1 to indicate a failure due to the assertion.
        print(e)
        exit(1)
    # Exit with code 0 to indicate success.
    exit(0)
```

This script directly addresses the issue highlighted, where in-place addition of two `xarray.DataArray` objects with the same dimensions but different orders of coordinates fails. If the issue is present, it will trigger an `AssertionError` after printing the stack trace of the exception caught during the failing operation. If the in-place addition works as expected without raising any exceptions, the script will indicate that the test passed and exit with code 0, signifying that the issue is resolved.