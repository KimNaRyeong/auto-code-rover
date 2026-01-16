```python
# reproducer.py
import os
import django
from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

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

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',
    ),
    USE_TZ=True,
)

django.setup()

# Define models
class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

# Migrate models
from django.core.management import call_command
call_command("makemigrations", "__main__")
call_command("migrate", "__main__")

def reproduce_issue():
    try:
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()
            assert not Order.objects.filter(product_id="").exists(), "Order with empty product_id exists"
            assert Order.objects.filter(product=order.product).exists(), "Order with correct product does not exist"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        raise

    # Scenario where the issue is fixed
    try:
        with transaction.atomic():
            order = Order()
            order.product = Product(sku="foo")
            order.product.save()
            order.save()
            assert Order.objects.filter(product=order.product).exists(), "Correct product association failed"
        print("Issue has been fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```