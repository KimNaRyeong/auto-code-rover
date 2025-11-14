Here is the reproducer script:

```python
import os
from django.db import transaction
from django.test import TestCase
from yourapp.models import Product, Order  # Replace 'yourapp' with your app name

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

class Reproducer(TestCase):
    def test_reproducer(self):
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()
            if not Order.objects.filter(product_id="").exists():  # Succeeds, but shouldn't
                raise AssertionError("Expected data loss for parents with non-numeric primary key")
            if not Order.objects.filter(product=order.product).exists():  # Fails
                raise AssertionError("Expected product to be saved correctly")

if __name__ == "__main__":
    try:
        Reproducer().test_reproducer()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

```

This script is a Django test case that reproduces the issue. It creates an `Order` instance with an empty `Product` instance, sets the `sku` of the product and saves it. Then it asserts that there are no orders with an empty `product_id`. If this assertion fails (i.e., there are orders with an empty `product_id`), it prints a stack trace and exits with code 1.

Please replace `'yourapp'` in the script with your actual app name.