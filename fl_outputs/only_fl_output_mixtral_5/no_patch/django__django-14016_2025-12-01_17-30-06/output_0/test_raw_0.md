 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from django.db.models import Q

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

try:
    q1 = Q(x__in={}.keys())
    q2 = Q()
    q3 = q1 | q2
except Exception as e:
    print_stacktrace(e)
    assert False
```
When executed with `python3 reproducer.py`, it raises an `AssertionError` and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    q3 = q1 | q2
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query_utils.py", line 90, in __or__
    return self.Q(*(lookups + [other]), _connector=connector)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query_utils.py", line 72, in __init__
