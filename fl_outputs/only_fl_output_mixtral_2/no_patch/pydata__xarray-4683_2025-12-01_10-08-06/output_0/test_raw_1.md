 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import xarray as xr
import traceback

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    xr_version = xr.__version__
    print(f"xarray version: {xr_version}")
    da = xr.DataArray([[1.0, 2.0], [3.0, 4.0]])
    try:
        result = da.astype(dtype='d', order='F').values.strides
    except Exception as e:
        print_stacktrace(e)
        assert False, "astype method lost its order parameter"
    else:
        assert False, "astype method should have raised an exception"
```
When executed with `python3 reproducer.py`, the script will print the following output if the issue is present:
```vbnet
xarray version: 0.16.2
Traceback (most recent call last):
  File "reproducer.py", line 17
    result = da.astype(dtype='d', order='F').values.strides
TypeError: astype() got an unexpected keyword argument 'order'
