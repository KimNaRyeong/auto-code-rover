```python
# reproducer.py
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

def main():
    try:
        url = "https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/swot_adac/FESOM/surf/fma.zarr"
        ds = xr.open_dataset(url, engine='zarr') # note that ds is not chunked but still uses lazy loading
        chunk_summary = ds.chunks
        # This should not trigger loading the entire array into memory.
        # So we assert that accessing chunks doesn't increase memory substantially.
        # As it's challenging to assert memory usage directly without adding significant complexity,
        # we check the behavior which triggers the issue i.e., dataset should remain lazily evaluated.
        for var in ds.data_vars:
            assert not ds[var].variable._in_memory, "Variable was loaded into memory!"
        print("No assertion errors, issue may be fixed or not present.")
    except AssertionError as e:
        print_stacktrace(e)
        raise  # Re-raise the assertion error to allow detection of failure.

if __name__ == '__main__':
    main()
```

This script attempts to reproduce the issue where accessing the `.chunks` attribute on an `xarray` dataset backed by Zarr appears to load the entire dataset into memory, contrary to expectations. It raises an `AssertionError` if any of the variables in the dataset have been loaded into memory, which would indicate that the issue is present. Otherwise, it reports that no assertion errors occurred, which could mean the issue might be fixed or not present under the tested conditions. The `print_stacktrace` function is used to display a stack trace when an error occurs for clearer identification of the issue's source.