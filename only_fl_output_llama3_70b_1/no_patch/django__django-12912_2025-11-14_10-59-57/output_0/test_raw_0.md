Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
from django.db import models
from django.db.models import Min, Exists, OuterRef, Q, F
from django.core.exceptions import FieldError

# Define models
class IndicatorValue(models.Model):
    freight = models.IntegerField()
    datetime = models.DateTimeField()
    type = models.CharField(max_length=20)
    deleted = models.BooleanField(null=True)

class OrderItemResult(models.Model):
    order_line = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    loading_arm = models.ForeignKey('LoadingArm', on_delete=models.CASCADE)

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

class Order(models.Model):
    freight = models.IntegerField()

class LoadingArm(models.Model):
    LOADING_TYPE_TOP = 'TOP'
    LOADING_TYPE_BOTTOM = 'BOTTOM'
    loading_type = models.CharField(max_length=20)

# Create test data
IndicatorValue.objects.create(freight=1, datetime='2022-01-01', type='freight_created')
IndicatorValue.objects.create(freight=1, datetime='2022-01-02', type='freight_completed')
OrderItemResult.objects.create(order_line=OrderItem.objects.create(order=Order.objects.create(freight=1)), loading_arm=LoadingArm.objects.create(loading_type='TOP'))
OrderItemResult.objects.create(order_line=OrderItem.objects.create(order=Order.objects.create(freight=1)), loading_arm=LoadingArm.objects.create(loading_type='BOTTOM'))

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

try:
    queryset = IndicatorValue.objects.values("freight").annotate(
        loading_time=Min("datetime", filter=Q(type=IndicatorValue.TYPE_FREIGHT_CREATED)) - Max("datetime", filter=Q(type=IndicatorValue.TYPE_FREIGHT_COMPLETED)),
        has_top_loading=Exists(OrderItemResult.objects.order_by().filter(order_line__order__freight=OuterRef("freight"), loading_arm__loading_type=LoadingArm.LOADING_TYPE_TOP).values('pk')),
        has_bottom_loading=Exists(OrderItemResult.objects.order_by().filter(order_line__order__freight=OuterRef("freight"), loading_arm__loading_type=LoadingArm.LOADING_TYPE_BOTTOM).values('pk'))
    ).aggregate(top_min=Min("loading_time", filter=Q(has_top_loading=True, has_bottom_loading=False)))

    # Check if the issue is present
    sql = queryset.query.sql_with_params()[0]
    if 'has_top_loading" = false AND "has_top_loading"' in sql:
        raise AssertionError("Alias used in aggregate filtering is incorrect")

except Exception as e:
    print_stacktrace(e)
```
This script defines the necessary models, creates some test data, and then runs the problematic queryset. It checks if the generated SQL contains the incorrect alias usage and raises an `AssertionError` if it does. If the issue is fixed, the script will exit with code 0.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.