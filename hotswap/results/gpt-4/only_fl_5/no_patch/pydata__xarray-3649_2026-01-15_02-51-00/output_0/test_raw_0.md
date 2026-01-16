Here's a Python script named `reproducer.py` that you can use to reproduce the issue as described. It attempts to combine three datasets with `combine_by_coords` and checks if the process raises a `ValueError`. If the issue persists, it will print a stack trace. When the issue is fixed, the script should exit with code 0 and not print anything.

```python
import numpy as np
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

def reproduce_issue():
    x1 = xr.Dataset(
        {
            "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
        },
        coords={"y": [0, 1], "x": [10, 20, 30]},
    )
    x2 = xr.Dataset(
        {
            "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
        },
        coords={"y": [2, 3], "x": [10, 20, 30]},
    )
    x3 = xr.Dataset(
        {
            "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
        },
        coords={"y": [2, 3], "x": [40, 50, 60]},
    )
    
    try:
        xr.combine_by_coords([x1, x2, x3])
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as error:
        sys.exit(1)  # Exit with error code to indicate issue is present
    print("Issue fixed.")
    sys.exit(0)  # Exit with code 0, indicating issue is fixed.
```

This script checks for the specific issue with `combine_by_coords` mentioned in your problem description. If the problem is not resolved in the xarray library, the `ValueError` is caught, a stack trace is printed, and an `AssertionError` is raised to signal that the issue is still present. When the issue is fixed, the script should complete without raising exceptions.