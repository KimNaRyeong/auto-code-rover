Here is the reproducer script:

```python
from django.db.models import OuterRef, Subquery
from django.db.models.expressions import F
from django.test import TestCase

class Document(models.Model):
    pass

class Checklist(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

class OwnershipTransfer(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

class Reproducer(TestCase):

    def test_reproducer(self):
        try:
            cls = Document.objects.filter(checklist__isnull=False).annotate(part=F('id')).values('checklist__customer', 'created')
            ots = Document.objects.filter(ownershiptransfer__isnull=False).annotate(part=F('id')).values('ownershiptransfer__ship_target__contact', 'created')
            self.annotate(owner=Subquery(cls.union(ots).values('owner')[:1]))
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Expected error not raised")

if __name__ == "__main__":
    try:
        Reproducer().test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
```

This script defines a simple Django model, and then attempts to reproduce the issue by using `union` on two QuerySets that reference OuterRef. If the error is raised, it prints the stack trace and exits with code 0.