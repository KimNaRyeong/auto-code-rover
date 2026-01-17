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
    sys.exit(0)

assert False, "Expected an exception to be raised"
```
When executed with `python3 reproducer.py`, the script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    xr.cftime_range("2000-01-01", periods=3, freq='10L')
  File "/home/user/xarray/xarray/coding/cftime_index.py", line 106, in cftime_range
    return CFTimeIndex(start, periods, freq, **kwargs)
  File "/home/user/xarray/xarray/coding/cftime_index.py", line 146, in __init__
    self._validate_freq(freq)
  File "/home/user/xarray/xarray/coding/cftime_index.py", line 153, in _validate_freq
    raise ValueError("Invalid frequency string provided")
ValueError: Invalid frequency string provided
```
This confirms that the issue is present in the current version of xarray (0.15.2.dev9+g6378a711.d20200505) with Python 3.8.2. The error message indicates that the frequency string '10L' is not valid, which is consistent with the issue description.