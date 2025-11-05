Here is the reproducer script:

```python
import django
from django.db import models, connection
from django.db.models import F, Count, Sum, Case, When, FloatField
from django.db.models.expressions import Subquery
from django.test import TestCase

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

class TestIssue(TestCase):
    def test_referenced_group_by_aggregation_over_annotation(self):
        Book = models.Model
        Author = models.Model

        total_books_qs = (
            Book.objects.filter(authors__pk=OuterRef("pk"))
            .order_by()
            .values("pk")
            .annotate(total=Count("pk"))
            .values("total")
        )

        annotated_authors = Author.objects.annotate(
            total_books=Subquery(total_books_qs.annotate(total=F("total")).values("total")),
            total_books_a=Subquery(total_books_qs.filter(name__istartswith="a").annotate(total=F("total")).values("total")),
        ).values(
            "pk",
            "total_books",
            "total_books_a",
        )

        totals = annotated_authors.aggregate(
            sum_total_books=Sum("total_books"),
            sum_total_books_a=Sum("total_books_a"),
            a_over_total_rate=Case(
                When(sum_total_books=0, then=0),
                default=Round((Sum("total_books_a") / Sum("total_books")) * 100, 2),
                output_field=FloatField(),
            ),
        )

        self.assertEqual(totals['sum_total_books'], 3)
        self.assertEqual(totals['sum_total_books_a'], 0)
        self.assertEqual(totals['a_over_total_rate'], 0)

if __name__ == "__main__":
    try:
        TestIssue().run()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script creates a simple Django model, and then uses that model to reproduce the issue. It runs the test case, and if an `AssertionError` is raised, it prints the stack trace and exits with code 1. If any other exception is raised, it also prints the stack trace and exits with code 1.