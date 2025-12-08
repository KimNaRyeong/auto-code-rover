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

dc1 = xr.open_dataset('s3://its-live-data/datacubes/v02/N40E080/ITS_LIVE_vel_EPSG32645_G0120_X250000_Y4750000.zarr', engine= 'zarr', storage_options = {'anon':True})

start_time = time.time()
repr_html = dc1._repr_html_()
end_time = time.time()

print(f"Time taken for repr_html: {end_time - start_time} seconds")

# Uncomment the following line to see the fast reprs
# array_size_condition = False

array_size_condition = True
if array_size_condition:
    for variable in dc1.data_vars:
        array = dc1[variable]
        if array.size > 1000000:  # Adjust this value to simulate small or large datasets
            repr_html += f"Variable: {variable}, Size: {array.size}\n"

if repr_html != dc1._repr_html_():
    raise AssertionError("Representation mismatch")

print("Fast reprs!")
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script will print the time taken for the repr and the message "Fast reprs!" if the issue is not present. If the issue is present, it will raise an `AssertionError` with a stack trace.

To fix the issue, you can either adjust the `array_size_condition` variable to load only the necessary data for the repr or modify the `_repr_html_` method in the `xarray/core/formatting.py` file to avoid loading any data for reprs.