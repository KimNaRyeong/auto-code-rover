Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Round, F, Sum, Case, When

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
    try:
        total_books_qs = (
            models.Book.objects.filter(authors__pk=models.OuterRef("pk"))
            .order_by()
            .values("pk")
            .annotate(total=models.Count("pk"))
            .values("total")
        )
        
        annotated_authors = models.Author.objects.annotate(
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
                output_field=models.FloatField(),
            ),
        )
        
        if totals['a_over_total_rate'] != 0:
            raise AssertionError("Expected a_over_total_rate to be 0")
    
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    print("Test passed")
    exit(0)

if __name__ == "__main__":
    test_referenced_group_by_aggregation_over_annotation()
```

This script sets up the necessary models and then runs the aggregation query. If the `a_over_total_rate` is not 0, it raises an `AssertionError`, prints the stack trace using the provided function, and exits with code 1. Otherwise, it prints "Test passed" and exits with code 0.