Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q, QuerySet

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
        from django.db.models import F
        Celebrity = models.Model
        ReservedName = models.Model

        class Celebrity(Celebrity):
            name = models.CharField(max_length=255)
            id = models.IntegerField()

        class ReservedName(models.Model):
            name = models.CharField(max_length=255)
            id = models.IntegerField()

        qs1 = Celebrity.objects.all()
        qs2 = ReservedName.objects.all()
        result = list(qs1.union(qs2).values_list('name').order_by(F('id')))
        if not result:
            raise AssertionError("Expected a non-empty result")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script sets up the models, creates two querysets, and then tries to execute the union of these querysets with `values_list` and ordering by an unannotated column. If the issue is present, it will print the stack trace and exit with code 1.