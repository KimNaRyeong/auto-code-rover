Here is the reproducer script:

```python
import django
from django.db import transaction
from django.test.utils import setup_test_environment
from django.core.exceptions import IntegrityError

setup_test_environment()

django.setup()

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
    with transaction.atomic():
        order = Order()
        order.product = Product(sku="")
        order.product.save()
        order.save()
    assert not Order.objects.filter(product_id="").exists(), "Expected no orders with empty product ID."
    print("Test passed.")
except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print_stacktrace(e)
    exit(1)

class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
```

This script sets up a test environment, defines the `Product` and `Order` models, and then attempts to reproduce the issue by creating an order with an unsaved product instance. If the assertion fails or any other exception is raised during the transaction commit, it prints the stack trace and raises the exception again.