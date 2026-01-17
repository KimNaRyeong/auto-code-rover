```python
# reproducer.py
import numpy as np
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

def reproduce_dataset_issue():
    try:
        test = xr.Dataset(coords={'xy': ['x', 'y']})
        original_dtype = test['xy'].dtype

        test['test'] = xr.DataArray(np.array([0, 0]), dims=['xy'])
        assert test['xy'].dtype == original_dtype, "Coordinate dtype changed after adding a data variable."
    except Exception as e:
        print_stacktrace(e)
        raise

def reproduce_concatenation_issue():
    try:
        da1 = xr.DataArray(data=np.arange(4).reshape([2, 2]), dims=["x1", "x2"],
                           coords={"x1": np.array([0, 1]), "x2": np.array(['a', 'b'])})
        da2 = xr.DataArray(data=np.arange(4).reshape([2, 2]), dims=["x1", "x2"],
                           coords={"x1": np.array([1, 2]), "x2": np.array(['c', 'd'])})

        da_joined = xr.concat([da1, da2], dim="x2")

        assert da_joined.coords["x1"].dtype == da1.coords["x1"].dtype, "dtype of 'x1' coord changed after concatenation"
        assert da_joined.coords["x2"].dtype == da1.coords["x2"].dtype, "dtype of 'x2' coord changed after concatenation"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        reproduce_dataset_issue()
        reproduce_concatenation_issue()
        print("All checks passed successfully.")
    except AssertionError as ae:
        print_stacktrace(ae)
        exit(1)
```

The above Python script `reproducer.py` aims to detect the issues mentioned regarding the changes in `dtype` of coordinates in an `xarray.Dataset` object. Below are the important points in the script:

1. **Defining a print function for stack traces**: For improved readability of the error message, the `print_stacktrace` function captures and displays the traceback information for any exceptions raised during the execution of the test functions.

2. **Test function for dataset issue**: In `reproduce_dataset_issue`, the script performs operations as per the first part of your description involving the addition of a `DataArray` to an `xarray.Dataset` and checks if the `dtype` of coordinates changes unexpectedly.

3. **Test function for concatenation issue**: In `reproduce_concatenation_issue`, a similar approach is followed for the second part of your description involving the concatenation of `DataArray` objects. It checks if the `dtype` of coordinates remains consistent before and after performing the `xr.concat` operation.

4. **Error handling and assertions**: Each test function includes assertions to validate if the `dtype` of the coordinates remains as expected. If the condition fails, an assertion error is raised with a relevant message. Any caught exceptions invoke the `print_stacktrace` function to print detailed information about the error context.

5. **Main block execution**: When executed, the script runs both test functions. If all checks pass, it prints a success message. If any assertion fails, the script will print a detailed stack trace for the encountered assertion error and exit with code 1, indicating a failure due to the presence of the issue.

This structured approach helps in systematic testing and debugging of specific issues within the given context, ensuring clarity and precision in error reporting.