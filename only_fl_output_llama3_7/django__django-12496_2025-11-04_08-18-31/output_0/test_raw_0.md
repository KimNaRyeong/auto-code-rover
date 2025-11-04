Here is the reproducer script:

```python
import os
import uuid
from django.db import models
from django.db.models import signals
from django.db.transaction import atomic
from django.test.utils import CaptureStdout

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from django.conf import settings
    settings.configure()

    class Parent(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        title = models.TextField()

    class Child(Parent):
        body = models.TextField()

    with CaptureStdout() as stdout:
        try:
            with atomic():
                child = Child.objects.create(title='Test', body='Test')
        except Exception as e:
            print_stacktrace(e)
            raise
    if not stdout.getvalue().startswith('INSERT INTO "app_child"'):
        raise AssertionError("Expected extra query")

if __name__ == '__main__':
    main()
```

This script sets up a Django environment, defines the `Parent` and `Child` models as described in the issue description, creates a new `Child` object with custom primary key, and checks if the expected extra query is present. If not, it raises an `AssertionError`.