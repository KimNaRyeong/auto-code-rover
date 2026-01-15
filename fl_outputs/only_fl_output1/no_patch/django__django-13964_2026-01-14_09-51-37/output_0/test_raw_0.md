```python
import os
import django
from django.conf import settings
from django.db import models, transaction

# Define the Django settings to configure your application
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    INSTALLED_APPS=[
        __name__,  # This script will be the app
    ],
    USE_TZ=True,
)

django.setup()

# Define the models according to the issue description
class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

    class Meta:
        app_label = __name__

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        app_label = __name__

# Function to print the exception stack trace
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

# Reproducing the issue
def reproduce_issue():
    # Create tables for the involved models
    with transaction.atomic():
        models.Model._meta.apps.clear_cache()
        models.Model._meta.base_manager_name = models.Model._meta.default_manager_name
        # Un-comment the following lines if the script is run more than once without dropping the database
        try:
            models.Model._meta.apps.get_models()
        except AttributeError:
            pass  # Ignore if tables already exist
        
        # Ensure that the database schema is created for the test models
        try:
            from django.core.management import call_command
            call_command('migrate', verbosity=0, interactive=False)
        except Exception as e:
            print_stacktrace(e)
            raise
    
    try:
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()
            assert Order.objects.filter(product__sku="").exists(), "Order with empty 'product__sku' should not exist."
            assert Order.objects.filter(product=order.product).exists(), "Order with existing 'product' should exist."
    except AssertionError as ae:
        print_stacktrace(ae)
        raise
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        os._exit(1)  # Exit with error if there was an exception
    else:
        print("Reproduction script completed successfully.")
        os._exit(0)  # Exit without error if the script completes successfully
```