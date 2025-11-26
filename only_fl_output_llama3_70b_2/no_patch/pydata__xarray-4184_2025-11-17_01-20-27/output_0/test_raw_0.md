Here is the standalone Python script `reproducer.py` to reproduce the issue:
```python
import pandas as pd
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

try:
    s = pd.Series(
        np.random.rand(100000),
        index=pd.MultiIndex.from_product([
            list('abcdefhijk'),
            list('abcdefhijk'),
            pd.DatetimeIndex(start='2000-01-01', periods=1000, freq='B')
        ])
    )

    cropped = s[::3]
    cropped.index = pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))

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

    assert proposed_version_adj.equals(current_version), "Proposed version is not equal to current version"

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script reproduces the issue by creating a MultiIndexed Series, converting it to an xarray using both the default `to_xarray()` method and the proposed alternative method, and then comparing the results. If the results are not equal, it raises an `AssertionError` with a stack trace of the issue.