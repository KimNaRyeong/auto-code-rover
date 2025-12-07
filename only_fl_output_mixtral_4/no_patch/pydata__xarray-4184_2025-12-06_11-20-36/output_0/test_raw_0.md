 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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

s = pd.Series(
    np.random.rand(100000),
    index=pd.MultiIndex.from_product([
        list('abcdefhijk'),
        list('abcdefhijk'),
        pd.DatetimeIndex(start='2000-01-01', periods=1000, freq='B'),
    ])
)

cropped = s[::3]
cropped.index=pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))

current_version = cropped.to_xarray()

proposed_version = (
    cropped
    .unstack('y')
    .to_xarray()
    .to_array('y')
)

proposed_version_adj = (
    proposed_version
    .assign_coords(y=proposed_version['y'].astype(object))
    .transpose(*current_version.dims)
)

try:
    assert current_version.equals(proposed_version_adj)
except AssertionError:
    print_stacktrace(AssertionError("to_xarray() result is incorrect when one of multi-index levels is not sorted"))
```
The script reproduces the issue by creating a MultiIndexed series and then converting it to an `xarray.Dataset` using both the default `to_xarray()` method and the proposed alternative method. The script then compares the two resulting datasets and raises an `AssertionError` if they are not equal.

To run the script, simply execute `python3 reproducer.py` in the terminal. If the issue is present, the script will print a stack trace of the `AssertionError`. If the issue is fixed, the script will exit silently with code 0.