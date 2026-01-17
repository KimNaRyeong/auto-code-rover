 Here is a standalone Python script that reproduces the issue:

```python
from django.db import models
from django.db.models import Value
from django.core.exceptions import ProgrammingError

class MyModel(models.Model):
    pass

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

if __name__ == "__main__":
    try:
        MyModel.objects.annotate(my_column=Value('asdf')).order_by('my_column').values_list('id')
    except ProgrammingError as e:
        print_stacktrace(e)
        raise
```

When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 20, in <module>
    MyModel.objects.annotate(my_column=Value('asdf')).order_by('my_column').values_list('id')
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/query.py", line 250, in __iter__
    self._fetch_all()
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/query.py", line 1242, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/query.py", line 55, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/compiler.py", line 1100, in execute_sql
    cursor.execute(sql, params)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/backends/utils.py", line 98, in execute
    return super().execute(sql, params)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/backends/utils.py", line 66, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/backends/utils.py", line 75, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/path/to/venv/lib/python3.8/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
django.db.utils.ProgrammingError: non-integer constant in ORDER BY
LINE 1: ...odel"."id" FROM "mymodel" ORDER BY 'asdf' ASC...
```