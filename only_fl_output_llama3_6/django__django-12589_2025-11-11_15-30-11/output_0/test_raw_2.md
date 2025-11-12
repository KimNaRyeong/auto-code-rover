Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import django
from django.db import models, connection
from django.db.models import Count, Q, Subquery, OuterRef
from django.db.models.functions import Count as CountFunc

django.setup()

class A(models.Model):
    bs = models.ManyToManyField('B', related_name="a", through="AB")
    pass

class B(models.Model):
    pass

class AB(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE, related_name="ab_a")
    b = models.ForeignKey(B, on_delete=models.CASCADE, related_name="ab_b")
    status = models.IntegerField()

class C(models.Model):
    a = models.ForeignKey(A, null=True, blank=True, on_delete=models.SET_NULL, related_name="c", verbose_name=_("a"))
    status = models.IntegerField()

def main():
    ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
    filter_conditions = Q(pk=1) | Q(ab_a__b=1)
    query = A.objects.filter(filter_conditions).annotate(status=Subquery(ab_query.values("status")), c_count=Count("c"))
    answer = query.values("status").annotate(total_count=Count("status"))

    try:
        print(answer.query)
        print(answer)
    except Exception as e:
        print_stacktrace(e)
        raise

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

This script sets up the models, defines the query, and then attempts to execute it. If an exception is raised (which should be a `ProgrammingError` due to the ambiguous column reference), it prints the stack trace using the provided function and raises the exception again.

Please note that this script requires Django 3.0 or later to run.