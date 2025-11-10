Here is the reproducer script:

```python
import django
from django.db import transaction
from django.test import TestCase

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
        django.setup()
        from yourapp.models import Product, Order  # Replace 'yourapp' with the actual app name
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()
            assert not Order.objects.filter(product_id="").exists()  # This should raise an AssertionError
        print_stacktrace(AssertionError)

if __name__ == "__main__":
    try:
        Reproducer().test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed. The issue is fixed.")
        exit(0)
```

Please replace `'yourapp'` with the actual name of your app in the Django project.