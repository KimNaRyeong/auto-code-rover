Here is the reproducer script in a code block:

```python
import django
from django.db import models
from django.db.models.functions import Round, Case, When, FloatField, Sum

django.setup()

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

def test_referenced_group_by_aggregation_over_annotation():
    class Book(models.Model):
        pass

    class Author(models.Model):
        pass

    total_books_qs = (
        Book.objects.filter(authors__pk=Author.objects.values("pk"))
            .order_by()
            .values("pk")
            .annotate(total=Count("pk"))
            .values("total")
    )

    annotated_authors = Author.objects.annotate(
        total_books=Subquery(total_books_qs.annotate(
                total_books=models.F("total")
        ).values("total_books")),
        total_books_a=Subquery(total_books_qs.filter(name__istartswith="a").annotate(
                total_books_a=models.F("total")
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
            When(sum_total_books=0, then=0),
            default=Round((Sum("total_books_a") / Sum("total_books")) * 100, 2),
            output_field=models.FloatField(),
        ),
    )

    if totals['a_over_total_rate'] == 0:
        raise AssertionError("Expected a non-zero value for 'a_over_total_rate'")

try:
    test_referenced_group_by_aggregation_over_annotation()
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

This script sets up the necessary models and then runs the aggregation query. If the issue is present, it raises an `AssertionError` with a stack trace.