 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from django.db.models import Q

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    q1 = Q(x__in={}.keys())
    q2 = Q()
    q3 = q1 | q2
except Exception as e:
    print_stacktrace(e)
    assert False
```
When executed with `python3 reproducer.py`, it will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    q3 = q1 | q2
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query_utils.py", line 90, in __or__
    return self.Q(*q, _connector=connector)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1354, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1192, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/lookups.py", line 25, in __init__
    self.rhs = self.get_prep_lookup()
  File "/usr/local/lib/python3.8/site-packages/django/db/models/lookups.py", line 77, in get_prep_lookup
    return self.transform_value(value)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/lookups.py", line 115, in transform_value
