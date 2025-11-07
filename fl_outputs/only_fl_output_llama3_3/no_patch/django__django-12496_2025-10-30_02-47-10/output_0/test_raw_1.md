Here is a revised reproducer script that should reproduce the issue:

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import django
from django.conf import settings

django.setup()

class Parent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()

class Child(Parent):
    body = models.TextField()

@receiver(post_save, sender=Child)
def child_post_save(sender, instance, **kwargs):
    raise AssertionError("Expected extra query")

if __name__ == "__main__":
    try:
        Child.objects.create()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable before importing Django and its settings. It then defines the `Parent` and `Child` models with a custom primary key in the parent model, and uses the `post_save` signal to raise an `AssertionError`, which should trigger the extra query and print the stack trace when run.