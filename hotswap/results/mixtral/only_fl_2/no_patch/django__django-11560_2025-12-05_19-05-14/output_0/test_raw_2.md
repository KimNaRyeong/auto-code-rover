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
When executed with `python3 reproducer.py`, the script should raise a `ValueError` and print a stack trace with the line number of the statement that raises the exception. The output should look like this:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/query.py", line 942, in filters
    return self._filter_or_exclude(filter_expr)
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/query.py", line 960, in _filter_or_exclude
    clone.query.add_q(Q(*lookups[i], **lookups[i + 1]))
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1358, in add_q
    clause, _ = self._add_q(where_part, Q())
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1386, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1316, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1166, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/lookups.py", line 20, in __init__
    self.rhs = self.get_prep_lookup()
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/lookups.py", line 70, in get_prep_lookup
    return self.transform_value(value)
  File "/path/to/virtualenv/lib/python3.8/site-packages/django/db/models/lookups.py", line 107, in transform_value
    raise ValueError("Lookups on ExtractYear on a DurationField fails because "
ValueError: Lookups on ExtractYear on a DurationField fails because ExtractYear has an optimisation where it compares the source date with a range of dates.
```
If the issue is fixed, the script should not raise any exception and print "No exception raised." instead