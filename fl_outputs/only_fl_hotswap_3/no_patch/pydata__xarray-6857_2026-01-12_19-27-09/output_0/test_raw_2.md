 Here's a standalone Python script `reproducer.py` to reproduce the described issue:

```python
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
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

try:
    result = da_withunits == da_withoutunits
except Exception as e:
    print_stacktrace(e)

print(da_withunits.frequency.units)
```

To run the script, execute `python3 reproducer.py`. The script will print the stack trace of the issue, as described in the original report.

The script demonstrates that using the built-in `==` operator for DataArray comparison modifies the DataArray with attributes, leading to unexpected behavior. The expected behavior is that the comparison should not modify the original DataArrays.