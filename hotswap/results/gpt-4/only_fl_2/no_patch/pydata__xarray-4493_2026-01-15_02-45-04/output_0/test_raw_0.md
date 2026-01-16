```python
# reproducer.py
import numpy as np
import xarray as xr
import dask.array as da


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


def check_dask_array_is_still_chunked_after_update():
    # First case: using DataSet.update
    foo = xr.DataArray(np.random.randn(3, 3), dims=("x", "y")).chunk()  # foo is chunked
    ds = xr.Dataset({"foo": foo, "bar": ("x", [1, 2, 3])})  # foo is still chunked here

    update_dict = {"foo": (("x", "y"), ds.foo[1:, :]), "bar": ("x", ds.bar[1:])}
    ds.update(update_dict)

    # Check if foo is still chunked after update
    assert dask.is_dask_collection(ds.foo.data), "foo is no longer chunked after DataSet.update"

    # Second case: DataSet constructor triggering computation
    x = da.random.randint(1, 10, size=(100, 25))
    ds = xr.Dataset(dict(a=xr.DataArray(x, dims=('x', 'y'))))
    assert isinstance(ds.a.data, da.Array), "DataSet constructor with DataArray should not trigger computation"

    ds2 = xr.Dataset(dict(a=(('x', 'y'), ds.a)))
    assert isinstance(ds2.a.data, da.Array), "Recreating dataset with the same array should not trigger computation to numpy.ndarray"


try:
    check_dask_array_is_still_chunked_after_update()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
print("All checks passed.")
```
This script checks for the presence of the described issues:

1. If updating a chunked `dask` `DataArray` within an `xarray.Dataset` causes the `DataArray` to lose its chunked nature.
2. If constructing an `xarray.Dataset` with a `dask` `DataArray` triggers computation of that array.

When either of these two conditions fails, it prints a stack trace of the issue and exits with code 1. If no issue is present, it prints "All checks passed." and exits with code 0. This script will be helpful in verifying whether or not the issue has been fixed in a particular environment.