Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import django
from django.db import models
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

def main():
    class Author(models.Model):
        pass

    class Book(models.Model):
        authors = models.ForeignKey(Author, on_delete=models.CASCADE)

    users_qs = Author.objects.annotate(
        total_things=Subquery(
            Book.objects.filter(authors_id=OuterRef("pk")).annotate(
                total_objs=F("total")
            ).values("total_objs")
        )
    )

    annotated_users = users_qs.annotate(
        sum_total_objs=Sum("total_things"),
        avg_conversion_rate=Case(
            When(
                sum_total_objs=0,
                then=0,
            ),
            default=Round(
                (Sum("sum_total_confirmed_objs") / Sum("sum_total_objs")) * 100, 2
            ),
            output_field=FloatField(),
        )
    )

    totals = annotated_users.aggregate(
        sum_total_objs=Sum("total_things"),
        avg_conversion_rate=Case(
            When(
                sum_total_objs=0,
                then=0,
            ),
            default=Round(
                (Sum("sum_total_confirmed_objs") / Sum("sum_total_objs")) * 100, 2
            ),
            output_field=FloatField(),
        )
    )

    if totals['avg_conversion_rate'] != 0:
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script should reproduce the issue by raising an `AssertionError` when run.