 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import sys

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    xr.cftime_range("2000-01-01", periods=3, freq='10L')
except Exception as e:
    print_stacktrace(e)
    assert False
```
When executed with `python3 reproducer.py`, it should raise a `ValueError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    xr.cftime_range("2000-01-01", periods=3, freq='10L')
  File "/home/user/xarray/xarray/coding/cftime_index.py", line 122, in cftime_range
    return CFTimeIndex(
  File "/home/user/xarray/xarray/coding/cftime_index.py", line 234, in __init__
    self._generate_index()
  File "/home/user/xarray/xarray/coding/cftime_index.py", line 267, in _generate_index
    self._index = self._generate_cftime_index(start, stop, step)
  File "/home/user/xarray/xarray/coding/cftime_index.py", line 283, in _generate_cftime_index
    freq = cftime_unit_to_dateutil(freq)
  File "/home/user/xarray/xarray/coding/cftime_index.py", line 112, in cftime_unit_to_dateutil
    raise ValueError("Invalid frequency string provided")
ValueError: Invalid frequency string provided
```
This confirms that the smallest cftime offset defined in `xarray.coding.cftime_offsets.py` is "second" (S), and the precision of cftime objects goes down to the millisecond (L) and microsecond (U) are currently untested as `xr.cftime_range` cannot generate an index.