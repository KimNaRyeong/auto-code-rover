Here is the reproducer script:

```python
import pandas as pd
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

def reproduce_issue():
    s = pd.Series(np.random.rand(100000), 
                  index=pd.MultiIndex.from_product([
                      list('abcdefhijk'),
                      list('abcdefhijk'),
                      pd.DatetimeIndex(start='2000-01-01', periods=1000, freq='B')
                  ]))

    cropped = s[::3]
    cropped.index = pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))

    current_method = cropped.to_xarray()
    proposed_version = (cropped.unstack('y').to_xarray().to_array('y'))
    
    try:
        assert current_method.equals(proposed_version_adj)
    except AssertionError as e:
        print_stacktrace(e)

reproduce_issue()
```

This script will raise an `AssertionError` if the issue is present, and it will print a stack trace of the issue.