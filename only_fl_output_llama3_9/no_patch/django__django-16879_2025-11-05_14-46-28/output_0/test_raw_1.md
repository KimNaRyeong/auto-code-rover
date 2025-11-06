Here is the reproducer script:

```python
import django
from django.db.models import F, Sum, Case, When, FloatField
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

def test_referenced_group_by_aggregation_over_annotation():
    class Book(django.db.models.Model):
        authors = django.db.models.ForeignKey('Author', on_delete=django.db.models.deals.DoNothing)
        total_books = django.db.models.IntegerField()

    class Author(django.db.models.Model):
        pk = django.db.models.AutoField(primary_key=True)
        total_books = django.db.models.IntegerField()
        total_books_a = django.db.models.IntegerField()

    Book.objects.create(authors__pk=1, total_books=2)
    Book.objects.create(authors__pk=1, total_books=3)
    Book.objects.create(authors__pk=2, total_books=4)

    annotated_authors = Author.objects.annotate(
        total_books=Subquery(Book.objects.filter(authors__pk=OuterRef("pk")).annotate(total=F("total")).values("total")),
        total_books_a=Subquery(Book.objects.filter(authors__pk=OuterRef("pk"), name__istartswith="a").annotate(total=F("total")).values("total"))
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
            output_field=FloatField(),
        ),
    )

    if totals['a_over_total_rate'] != 0:
        raise AssertionError("Expected a_over_total_rate to be 0")

try:
    test_referenced_group_by_aggregation_over_annotation()
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

This script creates some sample data, runs the aggregation query and checks if the result is what's expected. If not, it prints a stack trace of the issue and exits with code 1.