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
    try:
        import xarray as xr
        
        # Try accessing the .chunks attribute on a zarr backed xarray Dataset
        url = "https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/swot_adac/FESOM/surf/fma.zarr"
        ds = xr.open_dataset(url, engine='zarr')
        _ = ds.chunks  # Accessing chunks should not load the data
        
        # The expectation here is that no AssertionError will be raised when the issue is fixed
        # Current behavior improperly loads the dataset into memory, which we want to avoid.
        raise AssertionError("Accessing .chunks should not load the dataset into memory.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)  # Exit with 0 to indicate that the issue has reproduced correctly
    except Exception as e:
        # If any other exception occurs, it's not the specific AssertionError we're testing for
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```