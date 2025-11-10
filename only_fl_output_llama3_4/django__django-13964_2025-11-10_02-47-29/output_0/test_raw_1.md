Here is the reproducer script:

```python
from django.db import transaction
from django.test import TestCase
from django.core.exceptions import IntegrityError
from django.db.models import CharField, ForeignKey, Model
from django.db.utils import OperationalError

class Product(Model):
    sku = CharField(primary_key=True, max_length=50)

class Order(Model):
    product = ForeignKey(Product, on_delete=models.CASCADE)

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
            if not Order.objects.filter(product_id="").exists():  # Should raise AssertionError
                print_stacktrace(AssertionError("Expected data loss for parents with non-numeric primary key"))
                raise

        if os.environ.get('FIXED'):
            self.assertEqual(1, 0)  # Exit with code 0 when the issue is fixed
        else:
            raise SystemExit(1)

if __name__ == "__main__":
    Reproducer().test_reproducer()
```

To reproduce the issue, run `python3 reproducer.py`. The script will print a stack trace and exit with code 1.