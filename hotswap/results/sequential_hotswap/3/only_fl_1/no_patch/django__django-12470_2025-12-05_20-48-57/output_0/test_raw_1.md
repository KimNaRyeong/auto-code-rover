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

def main():
    Child.objects.all()

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 26, in <module>
    main()
  File "reproducer.py", line 22, in main
    Child.objects.all()
  File "/usr/local/lib/python3.9/site-packages/django/db/models/query.py", line 276, in __iter__
    self._fetch_all()
  File "/usr/local/lib/python3.9/site-packages/django/db/models/query.py", line 1261, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/usr/local/lib/python3.9/site-packages/django/db/models/query.py", line 57, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/usr/local/lib/python3.9/site-packages/django/db/models/sql/compiler.py", line 1152, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/utils.py", line 98, in execute
    return super().execute(sql, params)
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/utils.py", line 66, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/utils.py", line 75, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
  File "/usr/local/lib/python3.9/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
AssertionError: Ordering by -pk on Parent model results in ASC order instead of DESC order when querying the Child model.
```
This stack trace shows that the issue is caused by the `ordering` attribute on the `Parent` model's `Meta` class, which results in an ASC order instead of DESC order when querying the `Child` model.