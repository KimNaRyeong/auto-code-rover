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
    import psutil

    # URL to the Zarr dataset
    url = "https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/swot_adac/FESOM/surf/fma.zarr"
    
    try:
        before_memory_usage = psutil.Process().memory_info().rss

        ds = xr.open_dataset(url, engine='zarr', chunks={})
        # Trigger the computation which should not load the entire dataset
        _ = ds.chunks
        
        after_memory_usage = psutil.Process().memory_info().rss
        memory_difference = after_memory_usage - before_memory_usage

        # Raise an AssertionError if a significant increase in memory usage is detected
        assert memory_difference < 100 * 1024 * 1024, "Accessing chunks loads significant data into memory"
    
    except AssertionError as e:
        print_stacktrace(e)
        raise
    
    except Exception as e:
        print("An unexpected exception occurred.")
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```