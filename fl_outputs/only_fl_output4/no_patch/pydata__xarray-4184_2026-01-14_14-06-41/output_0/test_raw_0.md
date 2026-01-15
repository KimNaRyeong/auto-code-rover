```python
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
    import pandas as pd
    import numpy as np
    import xarray as xr

    # Create a MultiIndexed Series
    s = pd.Series(
        np.random.rand(100000), 
        index=pd.MultiIndex.from_product([
            list('abcdefhijk'),
            list('abcdefhijk'),
            pd.date_range(start='2000-01-01', periods=1000, freq='B'),
        ]))

    cropped = s[::3]
    cropped.index = pd.MultiIndex.from_tuples(cropped.index, names=list('xyz'))

    # Approach 1: Directly converting to xarray
    try:
        start_time = pd.Timestamp.now()
        current_method = cropped.to_xarray()
        end_time = pd.Timestamp.now()
        duration_direct = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds
    except Exception as e:
        print_stacktrace(e)
        raise

    # Approach 2: Using unstack and then converting to xarray
    try:
        start_time = pd.Timestamp.now()
        proposed_version = (
            cropped
            .unstack('y')
            .to_xarray()
            .to_array('y')
        )
        end_time = pd.Timestamp.now()
        duration_unstack = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds
    except Exception as e:
        print_stacktrace(e)
        raise

    proposed_version_adj = (
        proposed_version
        .assign_coords(y=proposed_version['y'].astype(object))
        .transpose(*current_method.dims)
    )

    # Check if both methods output the same result
    assert proposed_version_adj.equals(current_method), "The outputs of the two approaches are not the same."

    # Asserting the performance difference
    assert duration_direct > duration_unstack * 10, (
        "Direct conversion to xarray was not significantly slower than the unstack approach."
    )

    print(f"Direct method took: {duration_direct}ms")
    print(f"Unstack method took: {duration_unstack}ms")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    exit(0)
```

This script is designed to reproduce the issue related to performance differences between a direct conversion to xarray from a MultiIndex pandas series and a method involving unstacking before conversion. It first measures the time taken for both methods, compares the outputs to ensure they're identical, and finally asserts that the direct method should be significantly slower (the direct method's duration should be more than ten times the unstack method's duration). If the condition is not met or if there are any exceptions during the process, it prints a detailed stack trace.