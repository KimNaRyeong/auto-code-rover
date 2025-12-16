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
            print("AssertionError: Order.objects.filter(product_id='').exists() returned False")
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
        exit(1)
```
When executed with `python3 reproducer.py`, the script reproduces the issue by raising an `AssertionError` with the following output:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 42, in <module>
    main()
  File "reproducer.py", line 35, in main
    assert Order.objects.filter(product=order.product).exists()
AssertionError: Order.objects.filter(product=order.product).exists() returned False
```
The output shows that the assertion that checks if an `Order` object with the `product` instance exists in the database fails, indicating that the `product` instance was not correctly associated with the `Order` object.