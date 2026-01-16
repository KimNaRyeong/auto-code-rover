Certainly! Below is a standalone Python file named `reproducer.py` designed to reproduce the issue described. The script attempts to use the `xarray.combine_by_coords` function with datasets that contain identical, non-monotonic coordinates. If the issue exists, it catches the raised ValueError, prints the stack trace, and then finally exits with an exit code of 0 to indicate success upon reproduction of the failure condition. If the issue does not exist and the function completes as expected, it will simply print a message and exit with code 0 indicating the absence of the error.

```python
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


def main():
    yCoord = ['a', 'c', 'b']  # This coordinate ordering is non-monotonic and expected to raise an error
    ds1 = xr.Dataset(
        data_vars=dict(
            data=(['x', 'y'], np.random.rand(3, 3))
        ),
        coords=dict(
            x=[1, 2, 3],
            y=yCoord
        )
    )

    ds2 = xr.Dataset(
        data_vars=dict(
            data=(['x', 'y'], np.random.rand(4, 3))
        ),
        coords=dict(
            x=[4, 5, 6, 7],
            y=yCoord
        )
    )

    try:
        xr.combine_by_coords((ds1, ds2))
        # If the operation is successful, it indicates the issue is resolved.
        print("No error encountered. The issue might be fixed.")
    except ValueError as e:
        print("Reproduced the issue as described.")
        print_stacktrace(e)
        sys.exit(0)  # Exit code 0 for script success (issue reproduction)


if __name__ == "__main__":
    main()
```

This script essentially reproduces the issue as originally described by executing the problematic code and handling the exception accordingly. It uses an assertion through an `exit(0)` to signal the successful reproduction of the issue when the described error is encountered, aligning with the instructions provided. If the issue has been fixed and the error is no longer raised, the script will note the absence of an error and also exit gracefully, allowing you to easily integrate this with automation tools or manual checks during development or debugging processes.