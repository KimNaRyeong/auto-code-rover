```python
# reproducer.py
import numpy as np
import pandas as pd
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

def main():
    # Create a series with a MultiIndex
    s = pd.Series(
        np.random.rand(100000), 
        index=pd.MultiIndex.from_product([
            list('abcdefhijk'),
            list('abcdefhijk'),
            pd.DatetimeIndex(start='2000-01-01', periods=1000, freq='B'),
        ]))

    cropped = s[::3]
    cropped.index=pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))

    # Simple to_xarray()
    current_method = cropped.to_xarray()

    # Unstack in pandas first, then use to_array to do the equivalent of a restack
    proposed_version = (
        cropped
        .unstack('y')
        .to_xarray()
        .to_array('y')
    )

    # Adjust proposed_version to compare
    proposed_version_adj = (
        proposed_version
        .assign_coords(y=proposed_version['y'].astype(object))
        .transpose(*current_method.dims)
    )

    try:
        assert proposed_version_adj.equals(current_method), "The proposed version does not match the current_method"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
```