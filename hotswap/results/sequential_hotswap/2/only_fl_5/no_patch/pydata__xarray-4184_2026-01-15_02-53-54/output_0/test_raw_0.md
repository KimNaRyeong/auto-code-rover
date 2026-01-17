Below is a standalone Python script named `reproducer.py`, designed to encapsulate the described issues for easy reproduction. This script checks both issues: the performance discrepancy between using `.to_xarray()` directly and the alternative method involving `unstack` and `to_array`, as well as the incorrect order of multi-index levels when converting a `DataFrame` to an `xarray.Dataset`.

```python
import pandas as pd
import numpy as np
import time
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

def test_performance_issue():
    s = pd.Series(
        np.random.rand(100000),
        index=pd.MultiIndex.from_product([
            list('abcdefhijk'),
            list('abcdefhijk'),
            pd.date_range(start='2000-01-01', periods=1000, freq='B'),
        ]))

    cropped = s[::3]
    cropped.index = pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))

    start = time.time()
    current_method = cropped.to_xarray();
    time_current = time.time() - start

    start = time.time()
    proposed_version = (
        cropped
        .unstack('y')
        .to_xarray()
        .to_array('y')
    )
    time_proposed = time.time() - start

    try:
        assert time_current > time_proposed, "Performance issue not reproduced."
    except AssertionError as e:
        print_stacktrace(e)

def test_incorrect_order_issue():
    df = pd.concat(
        {
            'b': pd.DataFrame([[0, 1]], index=['foo'], columns=['C1', 'C2']),
            'a': pd.DataFrame([[2, 3]], index=['foo'], columns=['C1', 'C2']),
        }
    ).rename_axis(['lev1', 'lev2'])

    xarr = df.to_xarray()

    try:
        correct_order = ['b', 'a']
        xarr_order = xarr.lev1.values.tolist()
        assert xarr_order == correct_order, "Incorrect order of multi-index levels."
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_performance_issue()
    test_incorrect_order_issue()
```

When the issues are present, this script will raise `AssertionError`s and print detailed stack traces. For each of the functions (`test_performance_issue` and `test_incorrect_order_issue`), it uses assertions to check for the presence of the issues:

1. `test_performance_issue` measures the time taken for `.to_xarray()` and the alternative unstacking method, asserting that the former should be slower. If not, it indicates the performance issue may not be present.
2. `test_incorrect_order_issue` checks the order of multi-index levels after conversion to `xarray.Dataset`, asserting that the original order in the `DataFrame` must be preserved.

This script will exit with code 0 if both checks pass without any assertion failures.