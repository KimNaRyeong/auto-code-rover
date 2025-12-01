 Here is a standalone python script `reproducer.py` to reproduce the issue:
```python
import io
import numpy as np
from astropy.table import Table, Column

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

dtype = np.dtype([('z', 'f8'), ('name', 'f8'), ('y', 'i4')])
t = Table()
t['c'] = Column([(1, 2, 3), (4, 5, 6)], dtype=dtype)
out = io.StringIO()
t.write(out, format='ascii.ecsv')
print(out.getvalue())
try:
    t2 = Table.read(out.getvalue(), format='ascii.ecsv')
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, it raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 20, in <module>
    t2 = Table.read(out.getvalue(), format='ascii.ecsv')
  File "/Users/username/miniconda3/envs/astropy-dev/lib/python3.8/site-packages/astropy/table/connect.py", line 62, in __call__
    out = self.registry.read(cls, *args, **kwargs)
  File "/Users/username/miniconda3/envs/astropy-dev/lib/python3.8/site-packages/astropy/io/registry/core.py", line 212, in read
    data = reader(*args, **kwargs)
  File "/Users/username/miniconda3/envs/astropy-dev/lib/python3.8/site-packages/astropy/io/ascii/connect.py", line 18, in io_read
    return read(filename, **kwargs)
  File "/Users/username/miniconda3/envs/astropy-dev/lib/python3.8/site-packages/astropy/io/ascii/ui.py", line 396, in read
    dat = reader.read(table)
  File "/Users/username/miniconda3/envs/astropy-dev/lib/python3.8/site-packages/astropy/io/ascii/core.py", line 1403, in read
    table = self.outputter(self.header.cols, self.meta)
  File "/Users/username/miniconda3/envs/astropy-dev/lib/python3.8/site-packages/astropy/io/ascii/ecsv.py", line 232, in __call__
    out = serialize._construct_mixins_from_columns(out)
  File "/Users/username/miniconda3/envs/astropy-dev/lib/python3.8/site-packages/astropy/table/serialize.py", line 398, in _construct_mixins_from_columns
    _construct_mixin_from_columns(new_name, obj_attrs, out)
  File "/Users/username/miniconda3/envs/astropy-dev/lib/python3.8/site-packages/astropy/table/serialize.py", line 346, in _construct_mixin_from_columns
    data_attrs_map[val['name']] = name
TypeError: unhashable type: 'SerializedColumn'
```
This reproduces the issue described in the given report.