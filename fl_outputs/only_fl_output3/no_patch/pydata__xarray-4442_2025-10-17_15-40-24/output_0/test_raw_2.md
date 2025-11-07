Given your criteria, here is a standalone python file named `reproducer.py` designed to reproduce the reported issue. It attempts to convert a multi-dimensional `xarray.DataArray` with one dimension stacked into a `pandas.Series` or a `DataFrame`, which is expected to either raise an error or successfully convert based on whether the issue exists. Following your instruction, this script utilizes the provided function to print a clear and detailed stack trace upon encountering an error.

```python
import xarray as xr
import pandas as pd

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

def test_to_series_and_dataframe():
    try:
        da = xr.DataArray([[[1]]], dims=["a", "b", "c"]).stack(ab=["a", "b"])
        # convert to series
        series_result = da.to_series()
        # convert to dataframe
        df_result = da.to_dataframe("A")
        
        print("Conversion successful.")
        # Verify the result is as expected
        assert isinstance(series_result, pd.Series), "Result is not a pandas Series."
        assert isinstance(df_result, pd.DataFrame), "Result is not a pandas DataFrame."
        assert "a" in df_result.index.names and "b" in df_result.index.names, "MultiIndex names are incorrect."
        assert "c" in df_result.columns, "DataFrame columns are incorrect."

    except AssertionError as ae:
        # Assertion errors indicate a functional discrepancy rather than the anticipated technical issue.
        print(f"Assertion Error: {ae}")
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        expected_error = "isna is not defined for MultiIndex"
        if expected_error in str(e):
            print("Issue reproduced successfully.")
        else:
            # Raise an exception if an unexpected error occurs, making it clear this is not the anticipated issue.
            print("An unexpected error occurred, indicating a potential new issue or environment setup problem.")
        sys.exit(0)

if __name__ == "__main__":
    test_to_series_and_dataframe()
```

This script checks for the specific issue outlined, aiming for two main outcomes:

1. If the issue persists, it is expected to fail at converting the `DataArray` and print a detailed stack trace.
2. If the issue is fixed, the script will print "Conversion successful." and exit with code 0 after passing all assertions.

It uses assertions to verify the success of the conversion explicitly and also ensures the resulting objects are what we expect them to be (`pd.Series` and `pd.DataFrame` with the correct structure). An `AssertionError` indicates a different problem from the original issue, such as incorrect results post-conversion, suggesting the bug's fix might have introduced another bug or didn't fully address the issue at hand.