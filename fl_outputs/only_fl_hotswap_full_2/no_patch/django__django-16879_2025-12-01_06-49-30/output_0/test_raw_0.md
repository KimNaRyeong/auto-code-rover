 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import datetime

import django
from django.db import models
from django.db.models import Case, Count, FloatField, F, Q, Round, Sum, Subquery, Value as V
from django.db.models.functions import Coalesce

settings = django.conf.settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'tests',
    ],
)

from django.test.utils import setup_test_environment

setup_test_environment()
django.setup()

from django.test import SimpleTestCase


class OtherModel(models.Model):
    user = models.ForeignKey('tests.UserModel', on_delete=models.CASCADE)
    total = models.IntegerField(default=0)


class UserModel(models.Model):
    name = models.CharField(max_length=100)
    things = models.ManyToManyField(OtherModel, related_name='users')


class AggregationTestCase(SimpleTestCase):

    def test_referenced_group_by_aggregation_over_annotation(self):
        total_books_qs = (
            OtherModel.objects.filter(user__pk=OuterRef("pk"))
            .order_by()
            .values("pk")
            .annotate(total=Count("pk"))
            .values("total")
        )

        annotated_users = UserModel.objects.annotate(
            total_things=Subquery(total_books_qs.annotate(
                total_things=F("total")
            ).values("total_things")),
            total_things_a=Subquery(total_books_qs.filter(
                user__name__istartswith="a"
            ).annotate(
                total_things_a=F("total")
            ).values("total_things_a")),
        ).values(
            "pk",
            "total_things",
            "total_things_a",
        ).order_by("-total_things")

        totals = annotated_users.aggregate(
            sum_total_things=Sum("total_things"),
            sum_total_things_a=Sum("total_things_a"),
            a_over_total_rate=Case(
                When(
                    sum_total_things=0,
                    then=0,
                ),
                default=Round(
                    (Sum("total_things_a") / Coalesce(Sum("total_things"), V(1))) * 100, 2
                ),
                output_field=FloatField(),
            ),
        )

        self.assertEqual(totals['sum_total_things'], 3)
        self.assertEqual(totals['sum_total_things_a'], 0)
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
        AggregationTestCase.test_referenced_group_by_aggregation_over_annotation()
    except Exception as e:
        print_stacktrace(e)
        django.test.utils.dis