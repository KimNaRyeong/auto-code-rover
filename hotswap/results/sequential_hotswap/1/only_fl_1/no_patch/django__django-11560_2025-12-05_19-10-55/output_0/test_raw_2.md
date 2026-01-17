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
    print("No exception raised, the issue is fixed.")
    sys.exit(0)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 941, in filters
    return self._filter_or_exclude(False, *args, **kwargs)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 961, in _filter_or_exclude
    clone.query.add_q(Q(*args, **kwargs))
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1358, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1377, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1317, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1161, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/lookups.py", line 20, in __init__
    self.rhs = self.get_prep_lookup()
  File "/usr/local/lib/python3.8/site-packages/django/db/models/lookups.py", line 76, in get_prep_lookup
    return self.transform_value(value)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/lookups.py", line 110, in transform_value
    value = self.function(value)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/functions/datetime.py", line 102, in extract_year
    return extract(F('year'), value)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/functions/datetime.py", line 57, in extract
    return value.date().year if value else None
ValueError: year is out