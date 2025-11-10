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

def reproduce_issue():
    try:
        from django.db import models
        class ParentModel(models.Model):
            children = models.ManyToManyField('ChildModel')

        class ChildModel(models.Model):
            parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)

        parent = ParentModel.objects.create()
        child1 = ChildModel(parent=parent)
        child2 = ChildModel(parent=child1)
        parent.delete(keep_parents=True)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not reproduced")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a hierarchy of `ParentModel` and `ChildModel` instances, then attempts to delete the parent while preserving all relationships. If the issue is present, an `AssertionError` should be raised, which will be caught and printed with a stack trace.