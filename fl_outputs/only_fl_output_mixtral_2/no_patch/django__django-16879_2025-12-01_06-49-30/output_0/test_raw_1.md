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
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'tests',
    ],
)

django.setup()

from django.test import TestCase


class OtherModel(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    total = models.IntegerField()


class User(models.Model):
    name = models.CharField(max_length=100)


class TestReferencedGroupByAggregationOverAnnotation(TestCase):

    def setUp(self):
        User.objects.create(name='User 1')
        User.objects.create(name='User 2')
        User.objects.create(name='User 3')

        OtherModel.objects.bulk_create([
            OtherModel(user_id=1, total=1),
            OtherModel(user_id=1, total=2),
            OtherModel(user_id=1, total=3),
            OtherModel(user_id=2, total=4),
            OtherModel(user_id=2, total=5),
            OtherModel(user_id=3, total=6),
        ])

    def test_referenced_group_by_aggregation_over_annotation(self):
        total_books_qs = (
            OtherModel.objects.filter(user__pk=OuterRef("pk"))
            .order_by()
            .values("user")
            .annotate(total=Count("pk"))
            .values("total")
        )

        annotated_users = User.objects.annotate(
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

        self.assertEqual(totals['sum_total_things'], 12)
        self.assertEqual(totals['sum_total_things_a'], 3)
        self.assertEqual(totals['a_over_total_rate'], 25.0)


def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
       