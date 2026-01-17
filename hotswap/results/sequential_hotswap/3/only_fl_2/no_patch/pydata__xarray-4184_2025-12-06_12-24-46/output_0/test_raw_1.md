 I apologize for the mistake in the previous response. Here is the corrected `reproducer.py` script:
```python
import pandas as pd
import numpy as np
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    s = pd.Series(
        np.random.rand(100000),
        index=pd.MultiIndex.from_product([
            list('abcdefhijk'),
            list('abcdefhijk'),
            pd.DatetimeIndex(start='2000-01-01', periods=1000, freq='B'),
        ])
    )
    cropped = s[::3]
    cropped.index = pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))

    current_method = cropped.to_xarray()

    proposed_version = (
        cropped
        .unstack('y')
        .to_xarray()
        .to_array('y')
    )

    proposed_version_adj = (
        proposed_version
        .assign_coords(y=proposed_version['y'].astype(object))
        .transpose(*current_method.dims)
    )

    if not proposed_version_adj.equals(current_method):
        raise AssertionError("to_xarray() result is incorrect when one of multi-index levels is not sorted")

if __name__ == "__main__":
    try:
        reproduce_issue()
        print("Issue is fixed.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script reproduces the issue by creating a MultiIndexed series and comparing the results of two methods for converting it to an `xarray.Dataset`. The script raises an `AssertionError` if the results are not identical, indicating that the issue is present. The script exits with code 0 if the results are identical, indicating that the issue is fixed.