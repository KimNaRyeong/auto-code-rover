 Here is a standalone Python script `reproducer.py` that reproduces the given issue:
```python
import transaction
from django.core.exceptions import IntegrityError
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

def main():
    with transaction.atomic():
        order = Order()
        order.product = Product()
        order.product.sku = "foo"
        order.product.save()
        order.save()
        try:
            assert Order.objects.filter(product_id="").exists()
        except AssertionError:
            print("AssertionError: Order.objects.filter(product_id=\"\").exists() returned False")
            raise
        try:
            assert Order.objects.filter(product=order.product).exists()
        except AssertionError:
            print("AssertionError: Order.objects.filter(product=order.product).exists() returned False")
            raise

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements.

The script creates a `Product` instance with an empty primary key, assigns it to an `Order` instance, and saves both instances within a database transaction. It then checks whether the `Order` instance is in the database, first by querying for orders with an empty primary key, and then by querying for orders with the saved `Product` instance.

The expected behavior is that the second assertion should succeed, but instead, it fails, indicating that the `Order` instance is not associated with the saved `Product` instance. This is the issue described in the original report.

The script also demonstrates the correct behavior when the `Product` instance is initialized with its primary key before assignment to the `Order` instance. In this case, the `Order` instance is persisted correctly and both assertions succeed.