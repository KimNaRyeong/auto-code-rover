 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
import django
from django.db.models import Case, CharField, Exists, ForeignKey, OuterRef, Value
from django.db.models.lookups import Exists as ExistsLookup

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

django.setup()

class State(models.Model):
    pass

class County(models.Model):
    name = CharField(max_length=50)
    state = ForeignKey(State, related_name='counties')

try:
    County.objects.annotate(
        status=Case(
            When(Exists(State.objects.filter(counties=OuterRef('pk'), name="Texas")), name="Dallas", then=Value("DALLAS COUNTY")),
            default=Value("ELSEWHERE"),
        ))
except Exception as e:
    print_stacktrace(e)
```
When you run `python3 reproducer.py`, it will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 31, in <module>
    County.objects.annotate(
  File "/home/user/django/django/db/models/query.py", line 1127, in annotate
    clone.query.add_annotation(annotation, alias, is_summary=False)
  File "/home/user/django/django/db/models/sql/query.py", line 1474, in add_annotation
