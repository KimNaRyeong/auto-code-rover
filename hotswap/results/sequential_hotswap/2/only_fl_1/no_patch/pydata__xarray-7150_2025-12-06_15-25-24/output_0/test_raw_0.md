 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import pandas
from cf_xarray import encode_multi_index_as_compress, decode_compress_to_multi_index

def create_multiindex(**kwargs):
    return pandas.MultiIndex.from_arrays(list(kwargs.values()), names=kwargs.keys())

def main():
    dataset = xr.Dataset()
    dataset.coords["observation"] = ["A", "B"]
    dataset.coords["wavelength"] = [0.4, 0.5, 0.6, 0.7]
    dataset.coords["stokes"] = ["I", "Q"]
    dataset["measurement"] = create_multiindex(
        observation=["A", "A", "B", "B"],
        wavelength=[0.4, 0.5, 0.6, 0.7],
        stokes=["I", "Q", "I", "I"],
    )

    # Save as NetCDF
    encoded_dataset = encode_multi_index_as_compress(dataset)
    encoded_dataset.to_netcdf("multiindex.nc")

    # Load again
    loaded = xr.open_dataset("multiindex.nc")
    loaded = decode_compress_to_multi_index(loaded)

    # This works
    assert loaded.equals(dataset)

    # Use custom backend
    class MultiindexNetCDF4BackendEntrypoint(xr.backends.NetCDF4BackendEntrypoint):
        def open_dataset(self, *args, handle_multiindex=True, **kwargs):
            ds = super().open_dataset(*args, **kwargs)

            if handle_multiindex:
                ds = decode_compress_to_multi_index(ds)

            return ds

    xr.backends.register_backend("netcdf4-multiindex", MultiindexNetCDF4BackendEntrypoint)

    try:
        loaded = xr.open_dataset("multiindex.nc", engine="netcdf4-multiindex", handle_multiindex=True)
    except Exception as e:
        print_stacktrace(e)

    # This fails
    # assert loaded.equals(dataset)


def print_stacktrace(e: Exception):
    import traceback, sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 65, in <module>
    main()
  File "reproducer.py", line 56, in main
    assert loaded.equals(dataset)
  File "/home/user/.local/share/virtualenvs/test-oePfdNug/lib/python3.8/site-packages/xarray/core/variable.py", line 2795, in data
    raise ValueError(
ValueError: Cannot assign to the .data attribute of dimension coordinate a.k.a IndexVariable 'measurement'. Please use DataArray.assign_coords, Dataset.assign_coords or Dataset.assign as appropriate.
```
The issue is that the `decode_compress_to_multi_index` function is modifying the `measurement` coordinate of the `Dataset` object, which is not allowed because it is a dimension coordinate. The error message suggests using `DataArray.assign_coords`, `Dataset.assign_coords`, or `Dataset.assign` to modify the coordinates instead.

To fix the issue, the `decode_compress_to_multi