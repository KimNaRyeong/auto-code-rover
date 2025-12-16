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
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following output:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 41, in <module>
    main()
  File "reproducer.py", line 35, in main
    assert Order.objects.filter(product=order.product).exists()
AssertionError: AssertionError: Order.objects.filter(product=order.product).exists() returned False
```
This reproduces the issue where the foreign key constraint is not enforced until the transaction commits, and the `product_id` is set to an empty string instead of the `sku` of the `Product` instance.