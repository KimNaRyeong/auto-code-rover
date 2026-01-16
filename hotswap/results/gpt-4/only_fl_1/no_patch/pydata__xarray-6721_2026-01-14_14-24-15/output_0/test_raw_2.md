Given the new constraints and the requirement for improved accuracy in reproducing the issue based on the example provided, here's a more targeted standalone `reproducer.py` that attempts to replicate the issue of loading the entire dataset into memory when accessing the `chunks` attribute of a dataset loaded with `xarray` using the `zarr` engine. 

This script will perform a simple memory usage check before and after accessing the `.chunks` attribute. Please adjust the memory checking logic as needed based on the specific environment or for more precise measurements.

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

def get_memory_usage():
    # This function should return the current memory usage of the process.
    # Placeholder implementation - replace this with an actual memory measurement tool as appropriate.
    import os, psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # Return memory usage in MB.

def test_accessing_chunks_does_not_load_entire_dataset():
    try:
        import xarray as xr

        url = "https://ncsa.osn.xsede.org/Pangeo/pangeo-forge/swot_adac/FESOM/surf/fma.zarr"
        ds = xr.open_dataset(url, engine='zarr', chunks={})  # Ensure dataset is chunked

        initial_memory_usage = get_memory_usage()
        _ = ds.chunks  # Access chunks attribute
        final_memory_usage = get_memory_usage()

        memory_usage_increase = final_memory_usage - initial_memory_usage

        assert memory_usage_increase < 100, "Accessing chunks should not significantly increase memory usage"

    except AssertionError as e:
        print("AssertionError: This indicates that the issue is present.")
        print_stacktrace(e)
        exit(1)

    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        exit(1)

    print("Test passed: Accessing `chunks` does not significantly increase memory usage.")
    exit(0)

if __name__ == "__main__":
    test_accessing_chunks_does_not_load_entire_dataset()
```

Note: The `get_memory_usage` function in this example uses `psutil`, which is an external library not included in Python's standard library. You might need to install it separately using `pip install psutil` if you haven't already. Additionally, the memory usage test is quite simplistic; real-world scenarios might require more sophisticated approaches to accurately measure the memory impact of accessing the `.chunks` attribute.