Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import xarray
from copy import deepcopy

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

def test_copy_issue():
    ds = xarray.Dataset(
        coords={'x': ['foo'], 'y': ('x', ['bar'])},
        data_vars={'z': ('x', ['baz'])}
    )

    # Test Dataset.copy(deep=True)
    copied_ds_deep = ds.copy(deep=True)
    if not all(v.dtype.kind == 'U' for v in copied_ds_deep.coords.values()):
        raise AssertionError("Dataset.copy(deep=True) cast unicode indices to object")
    
    # Test DataArray.copy(deep=True/False)
    da = ds.z
    copied_da_deep = da.copy(deep=True)
    if not all(v.dtype.kind == 'U' for v in copied_da_deep.coords.values()):
        raise AssertionError("DataArray.copy(deep=True) cast unicode indices to object")
    copied_da_shallow = da.copy()
    if not all(v.dtype.kind == 'U' for v in copied_da_shallow.coords.values()):
        raise AssertionError("DataArray.copy() cast unicode indices to object")

try:
    test_copy_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script creates a sample `Dataset` and `DataArray` with unicode indices, then tests the `copy` method with both shallow and deep copying. If any of these tests fail, it raises an `AssertionError`, prints the stack trace, and exits with code 1. If all tests pass, it exits with code 0.

Please note that I've updated the script to use a more robust way to check if all coordinates have unicode dtype kind.