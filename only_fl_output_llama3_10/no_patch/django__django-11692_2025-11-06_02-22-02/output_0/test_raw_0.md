Here is the reproducer script:

```python
from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models.expressions import F

class Document(models.Model):
    pass

def main():
    cls = Document.objects.filter(checklist__isnull=False).annotate(part=F('id')).values('checklist__customer', 'created')
    ots = Document.objects.filter(ownershiptransfer__isnull=False).annotate(part=F('id')).values('ownershiptransfer__ship_target__contact', 'created')

    try:
        return cls.union(ots).values('owner')[:1]
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

if __name__ == "__main__":
    main()
```

This script defines a simple Django model `Document` and then attempts to use the `union` method on two QuerySets. The expected error is caught, printed with a stack trace using the provided function, and then an `AssertionError` is raised.