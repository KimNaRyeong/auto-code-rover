Here is the reproducer script:

```python
import os
import sys
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

class Parent(models.Model):
    name = models.CharField(max_length=256)

class ProxyParent(Parent):
    class Meta:
        proxy = True

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    many_to_many_field = models.ManyToManyField(
        to=Parent,
        through="ManyToManyModel",
        through_fields=['child', 'parent'],
        related_name="something"
    )

class ManyToManyModel(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='+')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='+')
    second_child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, default=None)

if __name__ == '__main__':
    try:
        Parent()
    except TypeError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
```

This script defines a custom reproducer that attempts to create an instance of the `Parent` model. If the issue is present, this will raise a `TypeError` due to the missing call to `make_hashable`. The script then prints a stack trace and exits with code 1 if the error occurs, or exits with code 0 if the test passes.

To use this script, save it as `reproducer.py` in your project directory, then execute it with Python: `python3 reproducer.py`. This will reproduce the issue if the fix is not present.