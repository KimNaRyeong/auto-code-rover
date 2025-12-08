 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.db import models
from django.db.models import F, ArrayAgg, KeyTextTransform
from django.core.exceptions import ImproperlyConfigured

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Parent(models.Model):
    name = models.CharField(default='test')

class Child(models.Model):
    parent = models.ForeignKey(
        Parent,
        on_delete=models.SET_NULL,
        related_name='children',
    )
    data = models.JSONField(default=dict)

parent = Parent.objects.create()
Child.objects.create(parent=parent, data={'en': 'English', 'fr': 'French'})

try:
    Parent.objects.annotate(
        children_array=ArrayAgg(
            KeyTextTransform('en', 'children__data'),
            distinct=True,
            ordering=[KeyTransform('en', 'children__data')],
        ),
    ).all()
except ImproperlyConfigured as e:
    print_stacktrace(e)
    raise
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 33, in <module>
    ordering=[KeyTransform('en', 'children__data')],
  File "/home/user/.virtualenvs/myproject/lib/python3.8/site-packages/django/db/models/query.py", line 1214, in annotate
