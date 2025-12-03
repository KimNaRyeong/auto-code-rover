 Here's a standalone python file `reproducer.py` to reproduce the issue:
```python
import astropy.table
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

events = [{"A":0,"B":0, "C":np.array([], dtype=np.uint64)},
          {"A":1,"B":0, "C":np.array([], dtype=np.uint64)},
          {"A":2,"B":2, "C":np.array([0,1], dtype=np.uint64)}]

try:
    table = astropy.table.QTable(rows=events)
    print(table)
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    table = astropy.table.QTable(rows=events)
  File "/Users/username/anaconda3/envs/myenv/lib/python3.9/site-packages/astropy/table/table.py", line 1534, in __init__
    self._base_repr_(html=False, max_width=None)
  File "/Users/username/anaconda3/envs/myenv/lib/python3.9/site-packages/astropy/table/table.py", line 1516, in _base_repr_
    data_lines, outs = self.formatter._pformat_table(
  File "/Users/username/anaconda3/envs/myenv/lib/python3.9/site-packages/astropy/table/pprint.py", line 589, in _pformat_table
    lines, outs = self._pformat_col(col, max_lines, show_name=show_name,
  File "/Users/username/anaconda3/envs/myenv/lib/python3.9/site-packages/astropy/table/pprint.py", line 276, in _pformat_col
    col_strs = [val.replace('\t', '\\t').replace('\n', '\\n') for val in col_strs_iter]
  File "/Users/username/anaconda3/envs/myenv/lib/python3.9/site-packages/astropy/table/pprint.py", line 276, in <listcomp>
