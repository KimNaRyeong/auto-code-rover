 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import os
import sys
import django
import your_project.settings as settings

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Initialize Django
os.chdir(os.path.dirname(__file__))
sys.path.append('')
django.setup()

# Create a test database
from django.core.management import call_command
call_command('migrate', '--noinput')

# Reproduce the issue
from testapp1.models import App1
from testapp2.models import App2

App1.objects.create(text='Test', another_app=App2.objects.create(text='Test'))
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script should raise an `AssertionError` with a stack trace.

The stack trace should look like this:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 33, in <module>
    App1.objects.create(text='Test', another_app=App2.objects.create(text='Test'))
  File "/usr/local/lib/python3.8/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 453, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 753, in save
    self.save_base(using=using, force_insert=force_insert,
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 790, in save_base
    updated = self._save_table(
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 895, in _save_table
    results = self._do_insert(cls._base_manager, using, fields, returning_fields, raw)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 933, in _do_insert
    return manager._insert(
  File "/usr/local/lib/python3.8/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 1254, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/compiler.py", line 1397, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 103, in execute
    return super().execute(sql, params)
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute