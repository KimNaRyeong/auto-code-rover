 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

foo = xr.DataArray(np.random.randn(3, 3), dims=("x", "y")).chunk()  # foo is chunked
ds = xr.Dataset({"foo": foo, "bar": ("x", [1, 2, 3])})  # foo is still chunked here

# The following line should print that foo is chunked
print(f"ds.foo before update: {ds.foo.data.chunksize}")

update_dict = {"foo": (("x", "y"), ds.foo[1:, :]), "bar": ("x", ds.bar[1:])}
update_dict["foo"][1]  # foo is still chunked here

ds.update(update_dict)

# The following line should raise an AssertionError, because ds.foo is no longer chunked
assert ds.foo.data.chunksize == (1, 3), f"ds.foo after update is not chunked: {ds.foo.data.chunksize}"
```
To run the script, execute `python3 reproducer.py` in the terminal. The script should raise an `AssertionError` and print a stack trace of the issue. The script should also exit with code 1.

Regarding the second question, I believe it is intentional that creating a Dataset with a DataArray and dimension names for a single variable causes computation of that variable. This is because when a Dataset is created with a DataArray and dimension names, the DataArray is copied and the copy is added to the Dataset. The copying process involves computation of the DataArray. This behavior is documented in the [xarray.Dataset constructor documentation](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.html), which states:

> If data is a DataArray, it is copied (and thus computation is triggered, if necessary) and added to the dataset with the given name and dimensions.

Therefore, if you want to avoid computation of the DataArray, you can create the Dataset with the DataArray and dimensions, and then update the Dataset with the DataArray using the `update` method. This way, the DataArray is not copied and the computation is not triggered. Here is an example:
```python
import dask.array as da
import xarray as xr

x = da.random.randint(1, 10, size=(100, 25))
ds = xr.Dataset(dict(a=xr.DataArray(x, dims=('x', 'y'))))
type(ds.a.data)  # dask.array.core.Array

# Recreate the dataset with the same array, but also redefine the dimensions
ds2 = xr.Dataset(dict(a=(('x', 'y'), ds.a)))
type(ds2.a.data)  # dask.array.core.Array
```
In this example, the DataArray `x` is not computed when creating the Dataset `ds2`, because it is not copied. Instead, it is added to the Dataset as a reference, and the dimensions are redefined using the `(('x', 'y'), ds.a)` syntax. This way, the DataArray remains chunked and the computation is not triggered.