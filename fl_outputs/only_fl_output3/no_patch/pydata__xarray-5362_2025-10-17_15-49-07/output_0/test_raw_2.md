Given the criteria and objectives outlined, here's a standalone Python script designed to meet your requirements. This script is constructed to specifically target and reproduce the issue where weighted operations in xarray do not raise an error when the dimensions passed do not exist. If the issue is present, it will raise an `AssertionError`. If the issue is resolved (i.e., an error is correctly raised when a nonexistent dimension is used), it will exit with code 0. The provided function to print stack traces is incorporated within the script to detail any exception thrown during its execution.

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
        ds = xr.Dataset({'air': (('x', 'y'), np.random.rand(4, 2))},
                         coords={'x': [10, 20, 30, 40],
                                 'y': [1, 2]})
        weighted_mean = ds.weighted(xr.ones_like(ds["air"])).mean("dummy_dim")
        raise AssertionError("Expected an error for invalid dimension but none occurred.")
    except KeyError as expected:
        # If the KeyError is raised, it means the dimension checking is working as expected.
        print("KeyError correctly raised for nonexistent dimension.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

Execution of this script involves trying to perform a weighted mean operation on a dataset with a dimension ("dummy_dim") that does not exist. According to the described issue, if the operation incorrectly proceeds without error, an `AssertionError` will be raised, indicating the presence of the bug. Conversely, if the implementation behaves correctly by raising a `KeyError` for the nonexistent dimension, the script will acknowledge this expected behavior and exit gracefully with code 0, signifying the issue's resolution.

Be mindful that this script is tailored to test the specific behavior of xarray based on the details provided and assumes that xarray and its dependencies are correctly installed in the execution environment.