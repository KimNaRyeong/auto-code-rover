Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
from django.db import models, connection
from django.db.models import F, Count, Round, FloatField, Sum, Case, When
from django.db.models.expressions import Subquery, OuterRef

class Author(models.Model):
    pass

class Book(models.Model):
    authors = models.ForeignKey(Author, on_delete=models.CASCADE)

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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script should reproduce the issue by raising an `AssertionError` when run.