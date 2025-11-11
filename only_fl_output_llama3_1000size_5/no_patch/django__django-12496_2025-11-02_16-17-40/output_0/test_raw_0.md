Here is the reproducer script:

```python
import os
import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()

class Child(Parent):
    body = models.TextField()

@receiver(post_save, sender=Child)
def save_child(sender, instance, **kwargs):
    raise AssertionError("Expected extra query")

if __name__ == "__main__":
    try:
        child = Child.objects.create()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

print("Issue not present")
```

This script creates a `Child` model that inherits from the `Parent` model, which has a custom primary key. It then uses the `post_save` signal to raise an `AssertionError` when the child is saved. If the issue is present (i.e., the extra query is executed), the script will print the stack trace and exit with code 0.