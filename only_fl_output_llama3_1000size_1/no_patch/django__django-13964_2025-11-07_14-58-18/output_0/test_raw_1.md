Here is the reproducer script:

```python
import django
from django.db import transaction
from django.test.utils import setup_test_environment
from yourapp.models import Product, Order

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

try:
    django.setup()
except ImportError as e:
    print_stacktrace(e)
    exit(1)

with transaction.atomic():
    order = Order()
    order.product = Product()
    order.product.sku = "foo"
    order.product.save()
    order.save()
assert not Order.objects.filter(product_id="").exists(), "Expected no orders with empty product ID"

try:
    order.save()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced")
exit(0)
```

This script should be placed in a file named `reproducer.py` and run using `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError`, print the stack trace of the issue, and then exit with code 1.