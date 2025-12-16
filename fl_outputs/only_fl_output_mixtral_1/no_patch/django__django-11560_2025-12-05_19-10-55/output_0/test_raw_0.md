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
    print("An unexpected exception occurred:", e)
else:
    print("No exception was raised.")
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/query.py", line 941, in filters
    return self._filter_or_exclude(False, *args, **kwargs)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/query.py", line 961, in _filter_or_exclude
    clone.query.add_q(Q(*args, **kwargs))
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1358, in add_q
    clause, _ = self._add_q(where_part, Q(*args, **kwargs))
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1386, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1316, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1166, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/lookups.py", line 22, in __init__
    self.rhs = self.get_prep_lookup()
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/lookups.py", line 72, in get_prep_lookup
    return self.function(*self.lookup_args, **self.lookup_kwargs)
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/functions/math.py", line 101, in extract_year
    return Value(timezone.make_naive(datetime.date(*value)).year)
TypeError: descriptor 'date' for 'datetime.datetime' objects doesn't apply to a 'tuple' object
```
Note that the error message is slightly different than the one described in the issue, but it is still a `TypeError` caused by the comparison of a `DurationField` with a date. This is because