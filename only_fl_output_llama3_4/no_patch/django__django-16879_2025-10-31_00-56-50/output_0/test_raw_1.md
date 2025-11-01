Here is a standalone Python file `reproducer.py` to reproduce the issue:

```python
import django
from django.db import models, connection
from django.db.models import F, Count, Sum, Case, When, FloatField
from django.db.models.expressions import Subquery, OuterRef

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
    class Book(models.Model):
        pass

    class Author(models.Model):
        pass

    total_books_qs = (
        Book.objects.filter(authors__pk=OuterRef("pk"))
        .order_by()
        .values("pk")
        .annotate(total=Count("pk"))
        .values("total")
    )

    annotated_authors = Author.objects.annotate(
        total_books=Subquery(total_books_qs.annotate(
            total_books=F("total")
        ).values("total_books")),
        total_books_a=Subquery(total_books_qs.filter(
            name__istartswith="a"
        ).annotate(
            total_books_a=F("total")
        ).values("total_books_a")),
    ).values(
        "pk",
        "total_books",
        "total_books_a",
    ).order_by("-total_books")

    totals = annotated_authors.aggregate(
        sum_total_books=Sum("total_books"),
        sum_total_books_a=Sum("total_books_a"),
        a_over_total_rate=Case(
            When(
                sum_total_books=0,
                then=0,
            ),
            default=Round(
                (Sum("total_books_a") / Sum("total_books")) * 100, 2
            ),
            output_field=FloatField(),
        ),
    )

    if totals['a_over_total_rate'] != 0:
        raise AssertionError("Issue not reproduced")

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present")
exit(0)
```

This script creates two model classes `Book` and `Author`, then defines a function `reproduce_issue()` that reproduces the issue. The function tries to aggregate the data using the same query as in the original issue, but with some minor modifications to make it standalone. If the issue is present (i.e., the calculated conversion rate is not 0), an `AssertionError` is raised and a stack trace is printed.