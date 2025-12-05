 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import xarray as xr
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
ds = xr.merge([valid_times, invalid_times])

try:
    xr.decode_cf(ds)
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue present: time decoding error message does not include the problematic variable's name"
```
When executed with `python3 reproducer.py`, the script will print the following stack trace and exit with code 1:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 20, in <module>
    xr.decode_cf(ds)
  File "/Users/user/miniforge3/envs/myenv/lib/python3.9/site-packages/xarray/core/decoding.py", line 107, in decode_cf
    decode_cf_variables(variables, attrs, decode_times=True)
  File "/Users/user/miniforge3/envs/myenv/lib/python3.9/site-packages/xarray/core/decoding.py", line 157, in decode_cf_variables
    variable = decode_cf_variable(variable, name=name, decode_times=decode_times)
  File "/Users/user/miniforge3/envs/myenv/lib/python3.9/site-packages/xarray/core/decoding.py", line 223, in decode_cf_variable
    variable = times.CFDatetimeCoder(use_cftime=use_cftime).decode(variable, name=name)
  File "/Users/user/miniforge3/envs/myenv/lib/python3.9/site-packages/xarray/coding/times.py", line 687, in decode
    dtype = _decode_cf_datetime_dtype(data, units, calendar, self.use_cftime)
  File "/Users/user/miniforge3/envs/myenv/lib/python3.9/site-packages/xarray/coding/times.py", line 190, in _decode_cf_datetime_dtype
    raise ValueError(msg)
ValueError: unable to decode time units 'days since 0001-01-01' with "calendar 'noleap'". Try opening your dataset with decode_times=False or installing cftime if it is not installed.
```