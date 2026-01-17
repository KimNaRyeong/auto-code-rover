```python
import dask.array as da
import numpy as np
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


def test_chunk_preservation_after_update():
    # Create a chunked dask DataArray and include it in a Dataset.
    foo = xr.DataArray(np.random.randn(3, 3), dims=("x", "y")).chunk()
    ds = xr.Dataset({"foo": foo, "bar": ("x", [1, 2, 3])})

    # Ensure that 'foo' is chunked initially.
    assert dask.is_dask_collection(ds.foo.data), "Initially, 'foo' is not a dask array as expected."

    # Update the Dataset with sliced elements of 'foo' and 'bar'.
    update_dict = {"foo": (("x", "y"), ds.foo[1:, :]), "bar": ("x", ds.bar[1:])}
    ds.update(update_dict)

    # Test if 'foo' is still chunked after the update.
    try:
        assert dask.is_dask_collection(ds.foo.data), "'foo' is not chunked after update."
    except AssertionError as e:
        print_stacktrace(e)
        raise


def test_computation_on_dataset_construction():
    # Demonstrate that creating a Dataset from a dask-backed DataArray using dimensions
    # triggers the computation and converts it into a NumPy array.
    x = da.random.randint(1, 10, size=(100, 25))
    ds = xr.Dataset(dict(a=xr.DataArray(x, dims=('x', 'y'))))
    try:
        assert isinstance(ds.a.data, da.Array), "Data in 'ds' is not a dask array as expected."
        ds2 = xr.Dataset(dict(a=(('x', 'y'), ds.a)))
        assert isinstance(ds2.a.data, da.Array), "Data in 'ds2' is unexpectedly a NumPy array, not a dask array."
    except AssertionError as e:
        print_stacktrace(e)
        raise


if __name__ == "__main__":
    try:
        test_chunk_preservation_after_update()
        test_computation_on_dataset_construction()
    except AssertionError:
        exit(1)
    print("All tests passed successfully.")
    exit(0)

```

This script aims to reproduce the issues pointed out:
1. The first function `test_chunk_preservation_after_update` reproduces the issue where updating a dataset containing a chunked dask DataArray results in losing its chunked nature.
2. The second function `test_computation_on_dataset_construction` checks if creating a dataset from a dask-backed DataArray, specifying dimension names, causes the array to be evaluated and converted into a NumPy array, against the expectation.

For both tests, if the issue exists, the script will print a stack trace and raise an `AssertionError`. If the checks pass, indicating the issues have been resolved, the script prints a success message and exits with code `0`.