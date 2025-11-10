Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey, ContentGenericForeignKey

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

def main():
    try:
        base = Base.objects.create(title="foo")
        extended = Extended(base=base)
        Comment(content_object=extended).save()

        comment = Comment.objects.prefetch_related("content_object").get()
        print(comment.content_object)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

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

This script sets up the models, creates an instance of each model, and then attempts to prefetch the `content_object` field. If the issue is present, it will raise an exception, which will be caught by the script and printed with a stack trace.