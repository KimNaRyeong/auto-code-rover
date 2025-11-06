Here is the reproducer script:

```python
from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models.expressions import F

class Document(models.Model):
    pass

def main():
    cls = Document.objects.filter(checklist__isnull=False, part=OuterRef('id')).values('checklist__customer', 'created')
    ots = Document.objects.filter(ownershiptransfer__isnull=False, part=OuterRef('id')).values('ownershiptransfer__ship_target__contact', 'created')

    try:
        return self.annotate(owner=Subquery(cls.union(ots).values('owner')[:1]))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

if __name__ == "__main__":
    main()
```

This script will attempt to reproduce the issue by creating two QuerySets, `cls` and `ots`, and then trying to use the `union` method on them. If the issue is present, it will print a stack trace and raise an `AssertionError`.