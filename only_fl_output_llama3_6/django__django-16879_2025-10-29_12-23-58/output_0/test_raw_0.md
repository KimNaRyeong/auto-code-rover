Here is the reproducer script:

```python
import django
from django.db.models import Count, F, FloatField, Round, Sum, When
from django.db.models.expressions import Case, Subquery, OuterRef

django.setup()

class Book:
    pass

class Author:
    pass

def test_referenced_group_by_aggregation_over_annotation():
    total_books_qs = (
        [Book() for _ in range(3)],
        [Book() for _ in range(2)],
    )[
        0
    ].filter(authors__pk=OuterRef("pk"))
    .order_by()
    .values("pk")
    .annotate(total=Count("pk"))
    .values("total")

    annotated_authors = Author().annotate(
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
        print_stacktrace(AssertionError("Expected a_over_total_rate to be 0"))
    else:
        print("Test passed")

if __name__ == "__main__":
    test_referenced_group_by_aggregation_over_annotation()
```

This script sets up the `Book` and `Author` classes, defines the aggregation query as described in the issue description, and then runs the query. If the result of the query is not what's expected (i.e., `a_over_total_rate` is not 0), it prints a stack trace using the provided function.