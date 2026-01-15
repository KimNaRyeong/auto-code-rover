Understood, let's ensure the setup is as self-contained and directly runnable as possible, assuming a Django environment. This script now includes the necessary imports, model definition, and configuration setup inline. Please ensure this is aligned with your Django application settings (e.g., database configuration) and that you have Django installed in your environment.

This script, `reproducer.py`, aims to reproduce the issue exactly as described, raising an `AssertionError` when the issue is reproduced and printing a detailed stack trace of the issue.

```python
import os
import django
from django.conf import settings
from django.db import models, transaction
from django.core.management import execute_from_command_line

# Minimal Django settings necessary for running this script
settings.configure(
    INSTALLED_APPS=[
        '__main__', # Allow Django to pick up on the model definitions below
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    USE_TZ=True,
)

django.setup()

# Model definitions
class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

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

def test_reproducer():
    try:
        # Ensure the model tables are created
        execute_from_command_line(['manage.py', 'migrate'])

        # Test case to reproduce the issue
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()

            assert not Order.objects.filter(product_id="").exists(), \
                "Order with empty product_id exists, which should not."
                
            assert Order.objects.filter(product=order.product).exists(), \
                "Order with linked product should exist."

        print("Test executed successfully, no assertion errors.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(2)

if __name__ == '__main__':
    test_reproducer()
```

### Important notes:

- This script defines Django models inline and uses an SQLite database for simplicity. You might need to adjust database settings according to your configuration.
- Before running this script, ensure your environment has Django installed and is suitable for running Django scripts.
- The script tries to perform database migrations to ensure the `Product` and `Order` tables exist. Ensure this is compatible with your setup or pre-migrate these models as needed.
- If the issue is accurately reproduced, the script will exit with code 1 upon `AssertionError`, providing details about the failure through the stack trace.