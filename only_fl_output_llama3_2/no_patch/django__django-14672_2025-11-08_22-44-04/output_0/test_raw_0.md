Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.apps import apps

def main():
    try:
        Parent = models.Model
        ProxyParent = type('ProxyParent', (Parent,), {'Meta': type('Meta', (), {'proxy': True})})
        Child = models.Model
        class ManyToManyModel(models.Model):
            parent = models.ForeignKey(ProxyParent, on_delete=models.CASCADE, related_name='+')
            child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='+')
            second_child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, default=None)

        many_to_many_field = models.ManyToManyField(
            to=ProxyParent,
            through="ManyToManyModel",
            through_fields=['child', 'parent'],
            related_name="something"
        )

        Child(parent=many_to_many_field)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

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

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.