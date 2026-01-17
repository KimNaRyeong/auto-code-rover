Here's a `reproducer.py` script that addresses the issues you've outlined. This script attempts to reproduce both scenarios: the performance issue regarding `to_xarray()` on a multi-indexed series and the incorrect order of data when multi-index levels are not sorted before conversion. It will raise an `AssertionError` if the issues are present, providing a clear stack trace for debugging purposes.

```python
import pandas as pd
import numpy as np
import xarray as xr
import time

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

def test_performance():
    s = pd.Series(
        np.random.rand(100000), 
        index=pd.MultiIndex.from_product([
            list('abcdefhijk'),
            list('abcdefhijk'),
            pd.DatetimeIndex(start='2000-01-01', periods=1000, freq='B'),
        ]))
    cropped = s[::3]
    cropped.index = pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))
    
    start_time = time.time()
    current_method = cropped.to_xarray()
    current_time = time.time() - start_time

    start_time = time.time()
    proposed_version = (
        cropped
        .unstack('y')
        .to_xarray()
        .to_array('y')
    )
    proposed_time = time.time() - start_time

    if not proposed_time < current_time / 10:  # Expecting at least 10x improvement
        raise Exception("Performance improvement not achieved with the proposed method.")

def test_correctness():
    df = pd.concat({
        'b': pd.DataFrame([[0, 1]], index=['foo'], columns=['C1', 'C2']),
        'a': pd.DataFrame([[2, 3]], index=['foo'], columns=['C1', 'C2']),
    }).rename_axis(['lev1', 'lev2'])
    
    try:
        xarray_ds = df.to_xarray()
        correct_order = ["b", "a"]
        if not all(x == y for x, y in zip(xarray_ds.coords['lev1'].values, correct_order)):
            raise AssertionError("Multi-index levels are not in the original order after conversion.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

def main():
    try:
        test_performance()
        test_correctness()
        print("Both issues were successfully reproduced without errors.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script should be placed in the root directory of the project and executed with Python 3. It leverages the conditions described in your issues to assert the presence of the issues. When the issues are fixed (i.e., the performance of `.to_xarray()` is improved to expected levels and the correct order of data is maintained when converting a pandas DataFrame with non-sorted multi-index levels to xarray), it shouldn't raise an `AssertionError` and should exit gracefully.