Given your requirements and the need to navigate around the constraints from the earlier attempts, I'll aim to provide a more accurate `reproducer.py` script. This script should encapsulate the issue with `xarray`'s `to_dataframe` and `to_series` methods when there's a multi-index involved along with additional dimensions, and correctly handle exceptions as you described.

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

def reproduce_issue():
    import xarray as xr

    try:
        # Create a DataArray with multi-dimensional data and stack two of its dims
        da = xr.DataArray([[[1]]], dims=["a", "b", "c"]).stack(ab=["a", "b"])
        s = da.to_series()
        df = da.to_dataframe("A")

        # Check if the result is a DataFrame or Series with the expected MultiIndex
        assert isinstance(s.index, pd.MultiIndex), "to_series() did not return a MultiIndex"
        assert isinstance(df.index, pd.MultiIndex), "to_dataframe() did not return a MultiIndex"

        # If both assertions pass, we consider the issue fixed
        print("Issue appears to be fixed.")
        sys.exit(0)
    
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Ensure non-zero exit if the above assert fails

if __name__ == "__main__":
    reproduce_issue()
```

### Explanation

- This script attempts to create a `DataArray` using `xarray` with dimensions that are stacked to form a `MultiIndex`. It then tries to convert this array to both a pandas `DataFrame` and `Series`. 
- The `assert` statements verify whether the converted structures have a `MultiIndex` as expected. If not, it raises an AssertionError. 
- If any exception happens during this process (including AssertionError from the check or any other exception from the conversion functions), the `print_stacktrace` function is invoked, and the script ends with a non-zero exit code indicating failure.
- If the DataArray is successfully converted without exceptions and the assertions pass, the script prints a confirmation message and exits with code 0, indicating the issue is resolved.

Note: This script assumes you have a working environment with `xarray` and compatible versions of `pandas` and `numpy` installed. Please adjust the error handling as per your specific debugging or error-logging requirements.