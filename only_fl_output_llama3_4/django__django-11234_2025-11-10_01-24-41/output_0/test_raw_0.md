Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

django.setup()

class Base(models.Model):
    title = models.TextField()

class Extended(Base):
    base = models.OneToOneField(Base, on_delete=models.CASCADE, primary_key=True)

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.TextField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

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
    base = Base.objects.create(title="foo")
    extended = Extended.objects.create(base=base)
    Comment.objects.create(content_object=extended)
    comment = Comment.objects.prefetch_related("content_object").get()
    assert comment.content_object == extended
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced, everything looks good.")
exit(0)
```

This script sets up the models and then tries to prefetch the `content_object` field. If the issue is present, it raises an `AssertionError`, which is caught and a stack trace is printed.