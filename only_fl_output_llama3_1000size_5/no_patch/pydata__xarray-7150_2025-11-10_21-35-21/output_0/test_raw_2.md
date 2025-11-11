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
dataset.to_netcdf("multiindex.nc")

try:
    loaded = xr.open_dataset("multiindex.nc")
    loaded = loaded.decode_cf()
    assert loaded.equals(dataset), "The datasets are not equal"
except Exception as e:
    print_stacktrace(e)
finally:
    print("Reproducer script finished successfully")
```

This script will reproduce the issue and print a stack trace.