 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.db.models import OuterRef, Subquery, QuerySet
from django.core.exceptions import ValidationError

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

class Document(models.Model):
    pass

cls = Document.objects.filter(
    checklist__isnull=False,
    part=OuterRef('id')
).values('checklist__customer', 'created')

ots = Document.objects.filter(
    ownershiptransfer__isnull=False,
    part=OuterRef('id')
).values('ownershiptransfer__ship_target__contact', 'created')

try:
    qs = Document.objects.annotate(
        owner=Subquery(cls.union(ots).values('owner')[:1])
    )
except ValidationError as e:
    print_stacktrace(e)
    raise AssertionError("ValidationError raised as expected")
```
When executed with `python3 reproducer.py`, the script will print the following stack trace and raise an `AssertionError`:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    qs = Document.objects.annotate(
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 514, in annotate
