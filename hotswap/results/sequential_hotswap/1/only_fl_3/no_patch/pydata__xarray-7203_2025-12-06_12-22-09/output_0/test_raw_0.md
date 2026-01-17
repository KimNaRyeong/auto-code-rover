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

start_time = time.time()
dc1 = xr.open_dataset('s3://its-live-data/datacubes/v02/N40E080/ITS_LIVE_vel_EPSG32645_G0120_X250000_Y4750000.zarr', engine= 'zarr', storage_options = {'anon':True})
end_time = time.time()
print(f"Time taken to load the dataset: {end_time - start_time} seconds")

try:
    dc1._repr_html_()
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will load the dataset and print the time taken to load it. Then, it will attempt to display the repr of the dataset and raise an exception. The stack trace of the exception will be printed, showing the line numbers of the statements that caused the issue.

If the issue is fixed, the script should print the time taken to load the dataset and exit with code 0 without raising any exceptions.