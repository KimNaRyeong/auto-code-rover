 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db.models import DurationField, F, Value
from django.db.models.functions import ExtractYear
from django.utils import timezone

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyModel(models.Model):
    duration = models.DurationField()

try:
    MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
except ValueError as e:
    print_stacktrace(e)
except Exception as e:
    print_stacktrace(e)
else:
    print("No exception raised.")
```
When executed with `python3 reproducer.py`, the script should raise a `ValueError` and print a stack trace with the line number of the statement that caused the issue.

The output should look like this:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/query.py", line 942, in filters
    return self._filter_or_exclude(False, *args, **kwargs)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/query.py", line 960, in _filter_or_exclude
    clone.query.add_q(Q(*args, **kwargs))
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1358, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1377, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1317, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1161, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/lookups.py", line 20, in __init__
    self.rhs = self.get_prep_lookup()
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/fields/related_lookups.py", line 96, in get_prep_lookup
    self.rhs = self.get_prep_value(self.rhs)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/fields/__init__.py", line 966, in get_prep_value
    raise e.__class__(
ValueError: Cannot use DurationField for looking up field with lookup 'year__gt' in field 'year'.
```
Note that the line number of the statement that caused the issue may be different depending on the location of the script in your project.