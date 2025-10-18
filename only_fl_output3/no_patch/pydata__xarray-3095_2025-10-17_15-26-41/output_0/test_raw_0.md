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

def check_dataset_copy():
    ds = xarray.Dataset(
        coords={'x': ['foo'], 'y': ('x', ['bar'])},
        data_vars={'z': ('x', ['baz'])})

    ds_original_dtype = str(ds['x'].dtype)
    deep_copied_ds_dtype = str(ds.copy(deep=True)['x'].dtype)

    # Check if dtype has unintentionally changed after deep copy.
    assert ds_original_dtype == deep_copied_ds_dtype, f"Expected dtype '{ds_original_dtype}' but got '{deep_copied_ds_dtype}' after deep copy"

def check_dataarray_copy():
    ds = xarray.Dataset(
        coords={'x': ['foo'], 'y': ('x', ['bar'])},
        data_vars={'z': ('x', ['baz'])})
    da = ds['z']
    
    da_original_dtype = str(da.dtype)
    # TestDataArray copy
    deep_copied_da_dtype = str(da.copy(deep=True).dtype)

    # Check if dtype has unintentionally changed after deep copy.
    assert da_original_dtype == deep_copied_da_dtype, f"Expected dtype '{da_original_dtype}' but got '{deep_copied_da_dtype}' after deep copy"

if __name__ == "__main__":
    try:
        check_dataset_copy()
        check_dataarray_copy()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    exit(0)
```