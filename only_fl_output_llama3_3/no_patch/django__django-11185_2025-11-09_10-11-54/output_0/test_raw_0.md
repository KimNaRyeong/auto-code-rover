Here is the reproducer script:

```python
import django
from django.db import models

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ParentModel(models.Model):
    children = models.ManyToManyField('ChildModel')

class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)

def reproduce_issue():
    parent = ParentModel.objects.create()
    child1 = ChildModel(parent=parent)
    child2 = ChildModel(parent=child1)
    parent.delete(keep_parents=True)

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(0)
else:
    print("Issue not reproduced")
    exit(0)
```

This script creates a hierarchy of `ParentModel` and `ChildModel` instances, then attempts to delete the parent while preserving all relationships. If the issue is present, an `AssertionError` should be raised, which will be caught and printed with a stack trace.