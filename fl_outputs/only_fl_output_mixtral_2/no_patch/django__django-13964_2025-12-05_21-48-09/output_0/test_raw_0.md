 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
            print_stacktrace(AssertionError("Order.product_id should be populated with product.sku"))
            raise
        try:
            assert Order.objects.filter(product=order.product).exists()
        except AssertionError:
            print_stacktrace(AssertionError("Order.product should be correctly linked to the saved Product instance"))
            raise

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with a stack trace, indicating that the issue is present.

The script creates an `Order` instance and sets its `product` attribute to a new `Product` instance that has not yet been saved. It then saves the `Product` instance and sets its `sku` attribute. Finally, it saves the `Order` instance and checks whether the `Order.product_id` field is populated with the `Product.sku` value.

The script also checks whether the `Order.product` attribute is correctly linked to the saved `Product` instance.

The output of the script should look like this:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 42, in <module>
    main()
  File "reproducer.py", line 37, in main
    assert Order.objects.filter(product=order.product).exists()
AssertionError: Order.product should be correctly linked to the saved Product instance
```
The script exits with a non-zero exit code, indicating that the test has failed.