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
    df = pd.concat(
        {
            'b': pd.DataFrame([[0, 1]], index=['foo'], columns=['C1', 'C2']),
            'a': pd.DataFrame([[2, 3]], index=['foo'], columns=['C1', 'C2']),
        }
    ).rename_axis(['lev1', 'lev2'])

    print('df:\n', df, '\n')
    current_version = df.to_xarray()
    print('current_version:\n', current_version, '\n')

    proposed_version = (
        df.unstack('lev1')
        .to_xarray()
        .to_array('lev1')
    )

    proposed_version_adj = (
        proposed_version
        .assign_coords(lev1=proposed_version['lev1'].astype(object))
        .transpose(*current_version.dims)
    )

    assert proposed_version_adj.equals(current_version), "Proposed version is not equal to current version"

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script reproduces the issue by creating a MultiIndexed DataFrame, converting it to an xarray using both the default `to_xarray()` method and the proposed alternative method, and then comparing the results. If the results are not equal, it raises an `AssertionError` with a stack trace of the issue.