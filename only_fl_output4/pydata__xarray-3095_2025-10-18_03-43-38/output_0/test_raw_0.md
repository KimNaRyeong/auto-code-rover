```python
import xarray
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

def check_dtype(ds, expected_dtype, context):
    # Note: Change 'unicode' to 'U' if you are working with Python 3,
    # since 'unicode' is a Python 2-specific datatype name,
    # and '<U*' is a NumPy representation for Unicode strings in Python 3.
    target_dtype = np.dtype(expected_dtype)
    actual_dtype = ds.coords['x'].dtype
    assert actual_dtype == target_dtype, (
        f"In context {context}, expected dtype {expected_dtype} for 'x', "
        f"but got {actual_dtype}"
    )

def main():
    try:
        ds = xarray.Dataset(
            coords={'x': ['foo'], 'y': ('x', ['bar'])},
            data_vars={'z': ('x', ['baz'])}
        )

        # Initial check
        check_dtype(ds, '<U3', 'initial creation')

        # Shallow copy check
        ds_copy = ds.copy()
        check_dtype(ds_copy, '<U3', 'after shallow copy')

        # Deep copy check
        ds_deep_copy = ds.copy(deep=True)
        check_dtype(ds_deep_copy, '<U3', 'after deep copy')

        # DataArray shallow copy check
        da_copy = ds.z.copy()
        check_dtype(da_copy, '<U3', 'DataArray after shallow copy')

        # DataArray deep copy check
        da_deep_copy = ds.z.copy(deep=True)
        check_dtype(da_deep_copy, '<U3', 'DataArray after deep copy')

        print("No issue detected.")

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script checks for the specific regression issue mentioned, where `xarray.Dataset.copy(deep=True)` and related operations incorrectly cast Unicode indices (`dtype='<U*'`) to objects (`dtype='object'`). The `check_dtype` function ensures that the `dtype` of the `'x'` coordinate matches the expected Unicode string type after various copy operations. An assertion error is raised with a detailed stack trace if a discrepancy is found, indicating the presence of the bug.