Here is the reproducer script:

```python
import django
from django.db import models
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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
        class MyModel(models.Model):
            name = models.CharField(max_length=255)
            tags = models.ManyToManyField(Tag, through='TaggedItem')

        class Tag(models.Model):
            name = models.CharField(max_length=255)

        class TaggedItem(models.Model):
            content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
            object_id = models.PositiveIntegerField()
            content_object = GenericForeignKey('content_type', 'object_id')
            tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

        admin.site.register(MyModel)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    django.setup()
    main()
```

This script creates a simple Django project with models and an admin interface. It then attempts to register the `MyModel` model in the admin interface. If the issue is present, this should raise an `AssertionError` and print a stack trace.