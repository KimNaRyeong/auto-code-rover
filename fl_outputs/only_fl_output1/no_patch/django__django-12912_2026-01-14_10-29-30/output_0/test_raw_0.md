Here is a standalone script `reproducer.py` designed to setup a minimal Django environment, define the necessary models, and try to reproduce the issue outlined. If the issue is present, it will raise an `AssertionError` and provide a detailed stack trace as requested.

```python
import os
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_django():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import django
    from django.conf import settings

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=(
            'reproducer',
        ),
        TIME_ZONE='UTC',
        USE_TZ=True,
    )

    django.setup()

def main():
    try:
        from reproducer.models import IndicatorValue, OrderItemResult
        from django.db.models import Min, Max, Q, OuterRef, Exists
        from django.db import connection

        # Attempt to reproduce the issue
        query = IndicatorValue.objects.values("freight").annotate(
            loading_time=Min("datetime", filter=Q(type=IndicatorValue.TYPE_FREIGHT_CREATED)) - Max("datetime", filter=Q(type=IndicatorValue.TYPE_FREIGHT_COMPLETED)),
            has_top_loading=Exists(
                OrderItemResult.objects.order_by().filter(
                    order_line__order__freight=OuterRef("freight"), loading_arm__loading_type=OrderItemResult.LOADING_TYPE_TOP,
                ).values('pk')
            ),
            has_bottom_loading=Exists(
                OrderItemResult.objects.order_by().filter(
                    order_line__order__freight=OuterRef("freight"), loading_arm__loading_type=OrderItemResult.LOADING_TYPE_BOTTOM,
                ).values('pk')
            )
        ).aggregate(
            top_min=Min("loading_time", filter=Q(has_top_loading=True, has_bottom_loading=False))
        )

        with connection.cursor() as cursor:
            cursor.execute(str(query.query))
            row = cursor.fetchone()

        assert 'WHERE ("has_top_loading" = true AND "has_bottom_loading" = false)' in str(query.query), "Issue not reproduced."

        print("Issue reproduced successfully. Assertion passed.")

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    setup_django()

    # Mock models and app config to ensure the script can run standalone
    from django.apps import AppConfig
    from django.db import models

    class ReproducerConfig(AppConfig):
        name = 'reproducer'
        verbose_name = "Reproducer App"

    class IndicatorValue(models.Model):
        freight = models.CharField(max_length=255)
        datetime = models.DateTimeField()
        type = models.CharField(max_length=50)
        TYPE_FREIGHT_CREATED = 'freight_created'
        TYPE_FREIGHT_COMPLETED = 'freight_completed'

    class LoadingArm(models.Model):
        LOADING_TYPE_TOP = 'TOP'
        LOADING_TYPE_BOTTOM = 'BOTTOM'
        loading_type = models.CharField(max_length=50)

    class Order(models.Model):
        freight = models.CharField(max_length=255)

    class OrderItem(models.Model):
        order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class OrderItemResult(models.Model):
        order_line = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
        loading_arm = models.ForeignKey(LoadingArm, on_delete=models.CASCADE)
        LOADING_TYPE_TOP = LoadingArm.LOADING_TYPE_TOP
        LOADING_TYPE_BOTTOM = LoadingArm.LOADING_TYPE_BOTTOM

    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
```

This script assumes you have a Django environment setup. Before running this script:

1. Ensure Django is installed in your environment (`pip install Django`).
2. Adjust the `DATABASES` setting in the `setup_django()` function if necessary, to match your database setup.

If the script exits with code 0 and prints the assertion message, it indicates the issue has been successfully reproduced according to your instructions.