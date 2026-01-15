```python
# reproducer.py

import sys
import django
from django.conf import settings
from django.db import models, transaction
from django.core.management import execute_from_command_line

# Define a minimal Django configuration
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',  # Use an in-memory SQLite database
        }
    },
    INSTALLED_APPS=[
        __name__,  # Register this module as a Django app
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
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_migrations():
    execute_from_command_line(['manage.py', 'migrate'])

def reproduce_issue():
    # Initial setup: migrate the database
    run_migrations()

    # Reproduce the issue as described
    try:
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()

            # Test for the expected failure condition
            assert not Order.objects.filter(product__sku="").exists(), "Order with unassigned 'product__sku' unexpectedly exists."
            assert Order.objects.filter(product=order.product).exists(), "Order with assigned 'product' does not exist."

            # If no exception is raised, then the issue is resolved or not present
            print("Issues were not reproduced, it seems they are resolved or not present in this environment.")
            sys.exit(0)

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```