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

def test_accessing_chunks_does_not_load_data():
    import xarray as xr

    url = "https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/swot_adac/FESOM/surf/fma.zarr"
    ds = xr.open_dataset(url, engine='zarr')  # note that ds is not chunked but still uses lazy loading

    try:
        _ = ds.chunks  # Accessing chunks to see if it triggers the whole array to be loaded into memory
        loaded = sum(v.nbytes for v in ds.variables.values())
        assert loaded == 0, f"Data loaded into memory: {loaded} bytes."
    except AssertionError as e:
        print("AssertionError: The issue is present, entire dataset appears to be loaded into memory when accessing the `chunks` attribute.")
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero code to indicate the issue is present
    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        exit(1)

    print("The issue appears to be fixed, accessing `chunks` does not load the data into memory.")
    exit(0)

if __name__ == "__main__":
    test_accessing_chunks_does_not_load_data()
```

This script checks if the issue with accessing chunks in a Zarr-backed xarray dataset loading the entire array into memory is present. It attempts to access the `.chunks` attribute of a dataset and asserts that no data should be loaded into memory just by accessing this attribute. If the assertion fails, it indicates the presence of the issue by raising an `AssertionError` and prints a stack trace. If no error occurs, it concludes the issue might be fixed and exits with code 0.