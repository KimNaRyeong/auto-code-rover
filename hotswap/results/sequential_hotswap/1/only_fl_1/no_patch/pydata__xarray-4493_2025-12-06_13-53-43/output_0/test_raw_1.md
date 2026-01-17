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

def main():
    foo = xr.DataArray(np.random.randn(3, 3), dims=("x", "y")).chunk()  # foo is chunked
    ds = xr.Dataset({"foo": foo, "bar": ("x", [1, 2, 3])})  # foo is still chunked here

    print("foo before update:", type(ds.foo.data))

    update_dict = {"foo": (("x", "y"), ds.foo[1:, :]), "bar": ("x", ds.bar[1:])}
    update_dict["foo"][1]  # foo is still chunked here

    ds.update(update_dict)

    try:
        assert isinstance(ds.foo.data, da.Array), "ds.foo is no longer a dask array after update!"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with a stack trace, indicating that `ds.foo` is no longer a dask array after the update. This demonstrates the issue where `DataSet.update` causes chunked dask DataArray to evaluate its values eagerly.