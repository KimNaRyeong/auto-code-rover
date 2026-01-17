```python
import os
import django
from django.conf import settings
from django.db import models, connections
from django.db.models import Q, Min, Max, OuterRef, Exists
from django.db.models.functions import Now

# Minimal Django setup for standalone script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)
django.setup()

# Models definition
class IndicatorValue(models.Model):
    TYPE_FREIGHT_CREATED = 'freight_created'
    TYPE_FREIGHT_COMPLETED = 'freight_completed'

    datetime = models.DateTimeField(default=Now)
    freight = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=((TYPE_FREIGHT_CREATED, 'Freight Created'), (TYPE_FREIGHT_COMPLETED, 'Freight Completed')))

    class Meta:
        app_label = '__main__'


class Order(models.Model):
    freight = models.CharField(max_length=50)

    class Meta:
        app_label = '__main__'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        app_label = '__main__'


class LoadingArm(models.Model):
    LOADING_TYPE_TOP = 'TOP'
    LOADING_TYPE_BOTTOM = 'BOTTOM'
    loading_type = models.CharField(max_length=10, choices=((LOADING_TYPE_TOP, 'Top'), (LOADING_TYPE_BOTTOM, 'Bottom')))

    class Meta:
        app_label = '__main__'


class OrderItemResult(models.Model):
    order_line = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    loading_arm = models.ForeignKey(LoadingArm, on_delete=models.CASCADE)

    class Meta:
        app_label = '__main__'


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


# Migration (sort of)
with connections['default'].schema_editor() as schema_editor:
    schema_editor.create_model(IndicatorValue)
    schema_editor.create_model(Order)
    schema_editor.create_model(OrderItem)
    schema_editor.create_model(LoadingArm)
    schema_editor.create_model(OrderItemResult)

# Main functionality to reproduce the issue
try:
    query = IndicatorValue.objects \
        .values("freight") \
        .annotate(
            loading_time=Min("datetime", filter=Q(type=IndicatorValue.TYPE_FREIGHT_CREATED)) - Max("datetime", filter=Q(type=IndicatorValue.TYPE_FREIGHT_COMPLETED)),
            has_top_loading=Exists(OrderItemResult.objects.order_by().filter(order_line__order__freight=OuterRef("freight"), loading_arm__loading_type=LoadingArm.LOADING_TYPE_TOP).values('pk')),
            has_bottom_loading=Exists(OrderItemResult.objects.order_by().filter(order_line__order__freight=OuterRef("freight"), loading_arm__loading_type=LoadingArm.LOADING_TYPE_BOTTOM).values('pk'))
        ) \
        .aggregate(
            top_min=Min("loading_time", filter=Q(has_top_loading=True, has_bottom_loading=False))
        )

    # Assuming issue manifests as an exception or incorrect behavior, so this check might need adjustment.
    assert query['top_min'] is not None, "Query did not execute as expected due to aliasing issue."

except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print_stacktrace(e)
    raise

print("Issue not found or has been fixed.")
```

This Python script sets up a minimal Django environment, defines necessary models and tries to execute a complex query that should illustrate the described issue regarding incorrect alias usage in the aggregate filtering. If the described issue occurs (incorrect SQL generation leading to an alias conflict or a logical error evaluated by the `assert` condition), it should capture and print a stack trace for easier diagnosis. Otherwise, it concludes the issue has been fixed or could not be reproduced.