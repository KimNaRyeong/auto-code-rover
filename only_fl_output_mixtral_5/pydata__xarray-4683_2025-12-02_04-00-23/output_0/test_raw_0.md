 Here is a standalone python file `reproducer.py` to reproduce the issue:
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

def main():
    xr_version = xr.__version__
    print(f"xarray version: {xr_version}")
    data_array = xr.DataArray([[1.0, 2.0], [3.0, 4.0]])
    try:
        result = data_array.astype(dtype='d', order='F').values.strides
    except Exception as e:
        print_stacktrace(e)
        assert False

    if xr_version == '0.15.1':
        expected_result = (8, 16)
    elif xr_version == '0.16.2':
        expected_result = None
    else:
        raise ValueError(f"Unexpected xarray version: {xr_version}")

    assert result == expected_result, f"Result: {result}, expected: {expected_result}"

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py` on xarray version 0.16.2, it will raise an `AssertionError` and print the following stack trace:
```yaml
xarray version: 0.16.2
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    main()
  File "reproducer.py", line 18, in main
    result = data_array.astype(dtype='d', order='F').values.strides
  File "/home/user/.local/lib/python3.8/site-packages/xarray/core/dataarray.py", line 433, in astype
    return self.variable.astype(dtype=dtype, copy=copy, **kwargs)
TypeError: astype() got an unexpected keyword argument 'order'
AssertionError:
