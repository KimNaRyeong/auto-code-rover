 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

array = xarray.DataArray(
    [[1, 2], [3, 4]],
    dims=['x', 'y'],
    coords={'x': ['a', 'b']}
)
stacked = array.stack(z=['x', 'y'])
try:
    print(stacked.drop('z'))
except Exception as e:
    print_stacktrace(e)

print()

try:
    print(stacked.assign_coords(z=[1, 2, 3, 4]))
except Exception as e:
    print_stacktrace(e)
```
When executed with the current version of xarray (0.18.3.dev137+g96c56836), the script will raise a `ValueError` with the following stack trace:
```less
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    print(stacked.drop('z'))
  File "/Users/user/miniconda3/envs/xarray/lib/python3.9/site-packages/xarray/core/dataarray.py", line 2425, in drop
    ds = self._to_temp_dataset().drop(labels, dim, errors=errors)
  File "/Users/user/miniconda3/envs/xarray/lib/python3.9/site-packages/xarray/core/dataset.py", line 4590, in drop
    return self.drop_vars(labels, errors=errors)
  File "/Users/user/miniconda3/envs/xarray/lib/python3.9/site-packages/xarray/core/dataset.py", line 4549, in drop_vars
    assert_no_index_corrupted(self.xindexes, names)
  File "/Users/user/miniconda3/envs/xarray/lib/python3.9/site-packages/xarray/core/indexes.py", line 1394, in assert_no_index_corrupted
    raise ValueError(
ValueError: cannot remove coordinate(s) 'z', which would corrupt the following index built from coordinates 'z', 'x', 'y':
<xarray.core.indexes.PandasMultiIndex object at 0x148c95150>
```
This reproduces the issue described in the bug report.