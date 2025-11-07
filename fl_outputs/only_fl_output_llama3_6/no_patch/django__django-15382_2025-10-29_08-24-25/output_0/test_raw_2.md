Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q, Exists
from django.conf import settings

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

def reproduce_issue():
    try:
        settings.configure()
        from django.db.models import Q, Exists
        class MyModel(models.Model):
            name = models.CharField(max_length=255)

        qs = MyModel.objects.filter(Q(name='test') | ~Exists(MyModel.objects.none()), name='test')
        print(qs.query)
        assert len(qs) == 0, "Expected an empty queryset"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable before creating the Django model and running the query. This should allow the script to run without raising an exception due to missing settings.