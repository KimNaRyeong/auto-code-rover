Here is the reproducer script:

```python
import pandas as pd
import xarray as xr
import numpy as np

def main():
    s = pd.Series(
        np.random.rand(100000), 
        index=pd.MultiIndex.from_product([
            list('abcdefhijk'),
            list('abcdefhijk'),
            pd.DatetimeIndex(start='2000-01-01', periods=1000, freq='B'),
        ]))

    cropped = s[::3]
    cropped.index = pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))

    current_method = cropped.to_xarray()
    proposed_version = (
        cropped
        .unstack('y')
        .to_xarray()
        .to_array('y')
    )

    assert proposed_version.equals(current_version), "The two methods should produce the same result"
    print_stacktrace(AssertionError)

if __name__ == "__main__":
    main()

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

```

This script should be run with Python 3.7 or later, and it should raise an `AssertionError` when the issue is present.