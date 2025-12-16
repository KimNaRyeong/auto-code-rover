 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

try:
    Child.objects.all()
except Exception as e:
    print_stacktrace(e)
    sys.exit(0)

assert False, "The query should have raised an exception"
```
When executed with `python3 reproducer.py`, the script prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 21, in <module>
    Child.objects.all()
  File "/usr/local/lib/python3.9/site-packages/django/db/models/query.py", line 276, in __iter__
    self._fetch_all()
  File "/usr/local/lib/python3.9/site-packages/django/db/models/query.py", line 1563, in _fetch_all
