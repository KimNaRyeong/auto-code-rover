Certainly! Below is the `reproducer.py` script designed to test the described issue within a Django project environment. This script will raise an `AssertionError` if the issue is present, showing a detailed stack trace for debugging purposes. If the issue is fixed, the script will complete without error and exit with code 0.

Make sure your Django environment is properly set up and that this script is executed in the root directory of your Django project, where `manage.py` is located.

```python
import os
import django
from django.db import transaction, models
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

# Define the models required for this issue reproduction
class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

    class Meta:
        app_label = 'temporary'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        app_label = 'temporary'

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

def reproduce_issue():
    try:
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()
            assert Order.objects.filter(product_id="").exists(), "Order with empty product_id should not exist."
            assert Order.objects.filter(product=order.product).exists(), "Order with linked product should exist."

        with transaction.atomic():
            order = Order()
            order.product = Product(sku="foo")
            order.product.save()
            order.save()
            assert Order.objects.filter(product=order.product).exists(), "Should succeed with preassigned sku"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    else:
        print("Test passed; no issue found.")
        exit(0)
```

Replace `"your_project.settings"` with the actual path to your Django project's settings module. Additionally, this script uses temporary models (which aren't part of any actual app models file) for the purpose of reproducing the described issue, so make sure your Django project is configured to allow dynamic model creation, or alternatively, integrate these model definitions and the test function into a unit test within your Django project.

After running this script, if the issue is present as described, the script should raise an `AssertionError` and print a detailed stack trace to help pinpoint the source of the bug. If the script completes without error, it means the issue has been fixed or is not present.