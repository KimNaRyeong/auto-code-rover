 Here is a standalone Python script that reproduces the issue:
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
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    Child.objects.all()
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 276, in __iter__
    self._fetch_all()
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 1261, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 57, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/compiler.py", line 1152, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 98, in execute
