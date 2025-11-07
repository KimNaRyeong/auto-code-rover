Here is the standalone Python file `reproducer.py` to reproduce the issue:
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

try:
    da = xr.DataArray([[[1]]], dims=["a","b","c"]).stack(ab=["a", "b"])
    series = da.to_series()
    assert isinstance(series.index, pd.MultiIndex), "Expected a MultiIndex"
    df = da.to_dataframe("A")
    assert isinstance(df.index, pd.MultiIndex), "Expected a MultiIndex"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
```
This script creates a DataArray with three dimensions, stacks two of them, and then tries to convert it to a Series using `to_series()` and a DataFrame using `to_dataframe()`. If the issue is present, an `AssertionError` will be raised, and the stack trace will be printed. If the issue is fixed, the script will exit with code 0.

Please note that I added another assertion for `to_dataframe()` to ensure that the issue is also reproduced for DataFrames.