Here is the reproducer script:

```python
from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models.functions import OuterRef as DjangoOuterRef

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
        class Document(models.Model):
            pass

        cls = Document.objects.filter(checklist__isnull=False, part=DjangoOuterRef('id')).values('checklist__customer', 'created')
        ots = Document.objects.filter(ownershiptransfer__isnull=False, part=DjangoOuterRef('id')).values('ownershiptransfer__ship_target__contact', 'created')

        return cls.union(ots).values('owner')[:1]
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script defines a `Document` model and attempts to use the `union` method with an outer reference. If the issue is present, it will print the stack trace and raise an `AssertionError`.