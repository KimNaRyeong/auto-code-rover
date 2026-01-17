```python
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

def main():
    import xarray as xr
    import pandas as pd

    def create_multiindex_dataset():
        coords = {'observation': ['A', 'B'],
                  'wavelength': [0.4, 0.5, 0.6, 0.7],
                  'stokes': ['I', 'Q']}

        midx = pd.MultiIndex.from_product([coords['observation'], coords['wavelength'], coords['stokes']],
                                          names=['observation', 'wavelength', 'stokes'])

        # Filling with dummy data, respecting the MultiIndex shape
        data = xr.DataArray(range(len(midx)), coords=[midx], dims=['index'],
                            name='measurement')

        return xr.Dataset({'measurement': data})

    # Encode and decode functions are placeholders for actual implementations
    def encode_multi_index_as_compress(ds):
        # This function should encode the dataset accordingly to be saved to NetCDF
        return ds

    def decode_compress_to_multiindex(ds):
        # This function should decode the dataset after loading from NetCDF
        return ds

    ds_original = create_multiindex_dataset()
    encoded = encode_multi_index_as_compress(ds_original)
    encoded.to_netcdf('multiindex.nc', engine='netcdf4')

    try:
        loaded = xr.open_dataset('multiindex.nc', engine='netcdf4')
        decoded = decode_compress_to_multiindex(loaded)

        assert decoded.equals(ds_original)
    except AssertionError as e:
        print("AssertionError: Loaded dataset does not match the original dataset")
        print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```