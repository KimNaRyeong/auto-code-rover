 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import sys
import time

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    start_time = time.time()
    dc1 = xr.open_dataset('s3://its-live-data/datacubes/v02/N40E080/ITS_LIVE_vel_EPSG32645_G0120_X250000_Y4750000.zarr', engine= 'zarr', storage_options = {'anon':True})
    repr_time = time.time() - start_time
    print(f"DC1 repr time: {repr_time}s")
    start_time = time.time()
    # Comment the following line to see the difference in loading time
    array_size = dc1.sizes['time']
    load_time = time.time() - start_time
    print(f"Array size load time: {load_time}s")
    total_time = repr_time + load_time
    print(f"Total time: {total_time}s")
    assert total_time < 5, "Expected fast reprs, but took longer than 5 seconds."

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script will print the time taken to load the dataset and the time taken to load the array size. If the total time taken is greater than 5 seconds, it will raise an AssertionError and print a stack trace.

You can run the script with `python3 reproducer.py`. If the issue is present, it should raise an AssertionError and print a stack trace. If the issue is fixed, it should exit with code 0.