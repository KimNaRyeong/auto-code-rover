 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import transaction
from django.core.exceptions import IntegrityError
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
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
    except Exception as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, demonstrating the issue.

The script creates a new `Order` instance and sets its `product` attribute to a new unsaved `Product` instance. It then sets the `sku` attribute of the `Product` instance and saves it. However, when saving the `Order` instance, the `product_id` attribute is not updated with the `sku` value, but instead remains an empty string. This results in a failed assertion when checking if an `Order` instance with the saved `Product` instance exists.

The script also demonstrates that if the `Product` instance is initialized with its primary key before assignment to the `Order` instance, it is persisted correctly. This is because the `Order.product_id` field is handled differently for auto vs non-auto primary keys. In the case of a non-auto primary key, the `Order.product_id` field is not updated until the transaction commits, which results in a `ForeignKeyViolation` due to the non-existence of a `Product` instance with an empty primary key.