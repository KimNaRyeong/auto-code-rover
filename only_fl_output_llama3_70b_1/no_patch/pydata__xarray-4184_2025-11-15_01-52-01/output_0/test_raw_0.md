Here is the standalone Python file `reproducer.py` to reproduce the issue:
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

# Create a series with a MultiIndex
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

# Approach 1: Simple `.to_xarray()`
current_method = cropped.to_xarray()

# Approach 2: Unstack in pandas first, and then use `to_array` to do the equivalent of a restack
proposed_version = (
    cropped
    .unstack('y')
    .to_xarray()
    .to_array('y')
)

# Check if the two approaches produce identical results
if not proposed_version_adj.equals(current_method):
    raise AssertionError("The two approaches do not produce identical results")

print("Issue not present. The two approaches produce identical results.")
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.