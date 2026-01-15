```python
# reproducer.py

import os
import sys
import django
from django.conf import settings
from django.db import models, transaction
from django.apps import apps
from django.core.management.commands.migrate import Command as MigrateCommand

# Define the settings for Django
settings.configure(
    DEBUG=True,
    INSTALLED_APPS=['__main__'],  # Dynamically add the current file as an app
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    USE_I18N=True,
    USE_TZ=True,
    SECRET_KEY='a-secret-key',
)

django.setup()

# Dynamically create migrations for the current models
apps.populate(settings.INSTALLED_APPS)
MigrateCommand().execute()

# Define models
class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

    class Meta:
        app_label = '__main__'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        app_label = '__main__'

# Function to print the exception stack trace
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

# Reproduction of the issue
def reproduce_issue():
    try:
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()

            # Check if there's an order with an empty product_id or without correct product linkage
            assert Order.objects.filter(product_id="").exists() == False, "Empty product_id unexpectedly exists."
            assert Order.objects.filter(product=order.product).exists() == True, "Correctly linked product does not exist."

        print("No issues found. The problem might have been resolved.")
        sys.exit(0)

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```