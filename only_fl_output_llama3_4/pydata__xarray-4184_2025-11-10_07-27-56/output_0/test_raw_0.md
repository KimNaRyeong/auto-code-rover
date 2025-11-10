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

    try:
        current_method = cropped.to_xarray()
    except Exception as e:
        print_stacktrace(e)
        raise

    proposed_version = (cropped
                         .unstack('y')
                         .to_xarray()
                         .to_array('y'))

    try:
        proposed_version_adj = (proposed_version
                                 .assign_coords(y=proposed_version['y'].astype(object))
                                 .transpose(*current_method.dims))

        assert proposed_version_adj.equals(current_method), "The two methods should be equal"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by calling `to_xarray()` on a MultiIndexed pandas Series. If an exception is raised, it will print the stack trace and re-raise the exception.