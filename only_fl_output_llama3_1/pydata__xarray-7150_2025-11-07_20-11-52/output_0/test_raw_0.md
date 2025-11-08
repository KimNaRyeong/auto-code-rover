Here is the reproducer script:

```python
import xarray as xr
import pandas

def create_multiindex(**kwargs):
    return pandas.MultiIndex.from_arrays(list(kwargs.values()), names=kwargs.keys())

dataset = xr.Dataset()
dataset.coords["observation"] = ["A", "B"]
dataset.coords["wavelength"] = [0.4, 0.5, 0.6, 0.7]
dataset.coords["stokes"] = ["I", "Q"]
dataset["measurement"] = create_multiindex(
    observation=["A", "A", "B", "B"],
    wavelength=[0.4, 0.5, 0.6, 0.7],
    stokes=["I", "Q", "I", "I"],
)

# Saving as NetCDF
from cf_xarray import encode_multi_index_as_compress
patched = encode_multi_index_as_compress(dataset)
patched.to_netcdf("multiindex.nc")

# Custom Backend
class MultiindexNetCDF4BackendEntrypoint(xr.backends.NetCDF4BackendEntrypoint):
    def open_dataset(self, *args, handle_multiindex=True, **kwargs):
        ds = super().open_dataset(*args, **kwargs)

        if handle_multiindex:  # here is where the restore operation happens:
            ds = decode_compress_to_multi_index(ds)

        return ds

# Registering custom backend
xr.backends.register_backend("netcdf4-multiindex", MultiindexNetCDF4BackendEntrypoint())

try:
    loaded = xr.open_dataset("multiindex.nc", engine="netcdf4-multiindex", handle_multiindex=True)
    assert False, "Expected ValueError"
except ValueError as e:
    print_stacktrace(e)

loaded = xr.open_dataset("multiindex.nc", engine="netcdf4-multiindex", handle_multiindex=False)
loaded = decode_compress_to_multi_index(loaded)
assert loaded.equals(dataset), "Dataset not equal after loading and decoding"

print("Reproducer script finished")
```

This script creates a dataset with a multi-index, saves it to a NetCDF file, defines a custom backend for opening the file, and then attempts to load the file using the custom backend while handling the multi-index. If the issue is present, an `AssertionError` should be raised; otherwise, the script will print a message indicating that the dataset was loaded and decoded correctly.