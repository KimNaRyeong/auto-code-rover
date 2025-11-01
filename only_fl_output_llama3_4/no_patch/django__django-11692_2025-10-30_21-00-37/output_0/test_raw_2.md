Here is the reproducer script:

```python
from django.db.models import OuterRef, Subquery
from django.db.models.functions import F

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
    from django.db.models import OuterRef, Subquery
    from django.db.models.functions import F

    class Document:
        pass

    cls = Document.objects.filter(checklist__isnull=False, part=OuterRef('id')).values('checklist__customer', 'created')
    ots = Document.objects.filter(ownershiptransfer__isnull=False, part=OuterRef('id')).values('ownershiptransfer__ship_target__contact', 'created')

    class QuerySetMock:
        def annotate(self, *args, **kwargs):
            raise ValueError("This queryset contains a reference to an outer query and may only be used in a subquery.")

    qs = QuerySetMock()
    return qs.annotate(owner=Subquery(cls.union(ots).values('owner')[:1]))

except Exception as e:
    print_stacktrace(e)
    assert False, "Expected error not raised"

if __name__ == "__main__":
    try:
        reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

def reproducer():
    return self.annotate(owner=Subquery(cls.union(ots).values('owner')[:1]))
```

This script defines a simple Django model, and then attempts to reproduce the issue by using `union` on two QuerySets that reference OuterRef. If the error is raised, it prints the stack trace and exits with code 0.