```python
"""
reproducer.py

This script attempts to reproduce an issue where saving a parent object after setting
on a child object leads to data loss for parents with non-numeric primary keys.

"""
import os
import sys
import django
from django.db import models, transaction
from django.core.exceptions import ValidationError

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


def print_stacktrace(e: Exception):
    import traceback
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
            # This assertion checks for the incorrect behavior where product_id is not set properly
            assert Order.objects.filter(product_id="").exists(), "Order with empty product_id exists."
            # This assertion is expected to fail, demonstrating the issue
            assert Order.objects.filter(product=order.product).exists(), "Order should reference the saved product."

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not reproduced, the relation is working as expected.")
        # In case the issue is fixed, we exit with code 0
        sys.exit(0)


if __name__ == "__main__":
    reproduce_issue()
```

Before running `python3 reproducer.py`, make sure you have a Django project set up with a `project/settings.py` file properly configured for your database. This script assumes the presence of a Django environment. The models `Product` and `Order` should be included in an app that has been created in the Django project, and this app should be added to the `INSTALLED_APPS` setting. Remember to run Django migrations to create the necessary database tables for these models before executing the script.

This script is intended to be run in a Django project environment where it interacts with Django's ORM to reproduce the specified issue. The script will raise an `AssertionError` if the issue is present and print a stack trace to provide clarity on where the issue occurs.