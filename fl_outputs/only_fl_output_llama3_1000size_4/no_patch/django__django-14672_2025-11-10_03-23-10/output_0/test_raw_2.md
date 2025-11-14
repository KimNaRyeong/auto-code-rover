Here is the standalone Python file `reproducer.py` to reproduce the issue:

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

def main():
    try:
        from django.db.models import ManyToManyRel
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

        m2m_rel = ManyToManyRel(through_fields=['child', 'parent'])
        print(m2m_rel.through_fields)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

This script attempts to create a `ManyToManyRel` object with the given `through_fields`. If an exception occurs during this process, it prints the stack trace using the provided function and exits with code 1.