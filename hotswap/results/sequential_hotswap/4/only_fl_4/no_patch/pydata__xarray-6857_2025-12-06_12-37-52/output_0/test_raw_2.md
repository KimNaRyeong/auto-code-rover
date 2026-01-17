 Here is a standalone python file `reproducer.py` to reproduce the issue:
```Python
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

da_withunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
da_withunits.frequency.attrs["units"] = "GHz"
print(da_withunits.frequency.units)
da_withoutunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
result = da_withunits == da_withoutunits
print(result)
try:
    print(da_withunits.frequency.units)
except Exception as e:
    print_stacktrace(e)
```
When executed with xarray version 2022.6.0, the script should print:
```css
GHz
<xarray.DataArray (frequency: 3)>
array([ True,  True,  True])
Coordinates:
  * frequency  (frequency) int32 1 2 3
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    print(da_withunits.frequency.units)
  File "...\AppData\Local\Programs\Python\Python39\lib\site-packages\xarray\core\common.py", line 256, in __getattr__
    raise AttributeError
AttributeError: 'DataArray' object has no attribute 'units'
```
This reproduces the issue where testing numerical equivalence of two DataArrays using the built-in operator '==' leads to mutilated DataArray.attrs dictionary. In this case, the DataArray `da_withunits` loses its `units` attribute after the comparison.