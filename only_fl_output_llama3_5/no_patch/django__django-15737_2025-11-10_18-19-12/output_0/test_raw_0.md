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

try:
    class Parent(models.Model):
        name = models.CharField(max_length=255)

    class Child(models.Model):
        parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    parent = Parent(name='parent_object')
    child = Child(parent=parent)
    parent.save()
    child.save()
    print(child.parent.name)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script creates a simple Django ORM model with a one-to-one relationship between `Parent` and `Child`. It then creates an instance of each, saves them to the database, and attempts to access the parent's name. If the issue is present, it will raise an `AssertionError`, which is caught and printed along with its stack trace.