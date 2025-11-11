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

from cf_xarray import encode_multi_index_as_compress
patched = encode_multi_index_as_compress(dataset)
patched.to_netcdf("multiindex.nc")

from cf_xarray import decode_compress_to_multi_index

def reproducer():
    loaded = xr.open_dataset("multiindex.nc", engine="netcdf4-multiindex", handle_multiindex=True)
    assert loaded.equals(dataset)  # This should raise an AssertionError
    print_stacktrace()

if __name__ == "__main__":
    reproducer()
```

This script creates a dataset with a multi-index, saves it to a NetCDF file, and then attempts to open the file using the custom `netcdf4-multiindex` engine. The assertion at the end should raise an AssertionError if the issue is present.

Please note that you need to have the necessary packages installed (xarray, pandas, etc.) and the `cf_xarray` module available for this script to run correctly.