Here is the reproducer script:

```python
import django
from django.db import transaction
from django.test.utils import setup_test_environment
setup_test_environment()

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

from django.db import models

class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

def reproduce_issue():
    try:
        with transaction.atomic():
            order = Order()
            order.product = Product(sku="foo")
            order.product.save()
            order.product.sku = "bar"
            order.product.save()
            order.save()
            assert not Order.objects.filter(product_id="").exists(), "Expected no orders with empty product ID."
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up a Django environment, defines the `Product` and `Order` models, and then attempts to reproduce the issue by creating an `Order`, setting its `product` attribute to a saved `Product` instance with a non-empty primary key, saving both objects, updating the product's primary key, saving again, and asserting that there are no orders with an empty product ID. If the assertion fails, it prints the stack trace of the exception and raises the exception again.

Please note that this script should be run in the root directory of a Django project where the models are defined.