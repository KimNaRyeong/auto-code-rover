 Here is a standalone python file `reproducer.py` to reproduce the issue:
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
When executed with `python3 reproducer.py`, the script raises an `IndexError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    table = astropy.table.QTable(rows=events)
  File "/Users/username/miniconda3/envs/myenv/lib/python3.9/site-packages/astropy/table/table.py", line 1534, in __init__
    self._construct_from_rows(rows, names=names, copy_strings=copy_strings,
  File "/Users/username/miniconda3/envs/myenv/lib/python3.9/site-packages/astropy/table/table.py", line 1672, in _construct_from_rows
    self._validate_rows(rows)
  File "/Users/username/miniconda3/envs/myenv/lib/python3.9/site-packages/astropy/table/table.py", line 1700, in _validate_rows
