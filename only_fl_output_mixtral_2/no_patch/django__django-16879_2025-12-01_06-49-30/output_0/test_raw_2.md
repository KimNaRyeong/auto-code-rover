 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import datetime

import django
from django.db import models
from django.db.models import Case, Count, FloatField, F, Q, Round, Sum, Subquery, Value as V
from django.db.models.functions import Coalesce

settings = django.conf.settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'tests',
    ],
    USE_TZ=True,
)

django.setup()

from django.test import SimpleTestCase


class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.datetime.now)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name='books')
    created_at = models.DateTimeField(default=datetime.datetime.now)


class tests(SimpleTestCase):

    def test_referenced_group_by_aggregation_over_annotation(self):
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

        self.assertEqual(totals['sum_total_books'], 3)
        self.assertEqual(totals['sum_total_books_a'], 0)
        self.assertEqual(totals['a_over_total_rate'], 0)


def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


if __name__ == '__main__':
    try:
        tests()
    except Exception as e:
        print_stacktrace(e)
        raise
```
This script creates a new SQLite database in memory, configures Django settings, and defines two models `Author` and `Book`. The test case `tests` is the same as the one provided in the issue description.

The script will raise an `