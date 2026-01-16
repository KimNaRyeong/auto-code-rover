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

def check_issue():
    import xarray as xr

    url = "https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/swot_adac/FESOM/surf/fma.zarr"
    ds = xr.open_dataset(url, engine='zarr')

    try:
        # Accessing chunks without loading the whole dataset into memory
        _ = ds.chunks
        # Since ds.chunks loaded the whole dataset, an AssertionError will not be raised
        raise AssertionError("Accessing `chunks` should not load the entire dataset.")
    except MemoryError as e:
        print("Detected a MemoryError as expected.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Issue is not fixed if any other exception is raised

if __name__ == "__main__":
    check_issue()
```

This script tries to reproduce the issue stated. The core of the problem revolves around the observation that accessing the `chunks` property on an `xarray` dataset backed by Zarr seems to load the entire dataset into memory, which is not the expected behavior. The `check_issue` function attempts to provoke this issue by accessing the `chunks` property and captures any exceptions related to this action. Specifically, it will:

- Attempt to access the `.chunks` attribute of a dataset.
- Assert an error condition that represents the undesired behavior of loading the entire dataset into memory when it shouldn't. Specifically, it raises an assertion error if accessing `.chunks` doesn't raise an exception tied to loading data into memory, implying that the action undesirably loads dataset into memory.

The script uses a try-except block to catch a `MemoryError` or any other exception that occurs when running the operation that is suspected to be problematic. If a `MemoryError` is caught, it indicates that the operation indeed attempts to load the entire dataset into memory, matching the user's report. Any other exception is handled by printing a detailed stack trace to aid in diagnosing the issue. This handling mechanism ensures that the script exits with code 1, signaling an error state unless the issue is resolved, and the specified assertion error can be raised without any uncaught exceptions occurring first.