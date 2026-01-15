To create a standalone Python file `reproducer.py` that demonstrates the described Django issue, we need to include setup for a minimal Django environment within the script. This means configuring Django settings, defining the models, and then reproducing the issue as described. Ensure Django is installed in your Python environment before running this script.

Below is the `reproducer.py`, including the needed Django environment setup, model definitions, and the logic to reproduce the specific issue regarding data loss when saving parent objects with non-numeric primary keys after setting on child objects.

```python
import os
import django
from django.conf import settings
from django.db import models, transaction
from django.core.management import call_command

# Configure minimal Django settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Define models
class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

# Implement the function to print stack trace
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

# Reproduce the issue
def reproduce_issue():
    try:
        call_command('makemigrations', interactive=False, verbosity=0)
        call_command('migrate', interactive=False, verbosity=0)

        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()

            assert Order.objects.filter(product_id="").exists(), "Expected an Order with an empty product_id to exist."
            assert Order.objects.filter(product=order.product).exists(), "Order with correct product does not exist."
            print("Issue not reproduced, no AssertionError.")
    except AssertionError as e:
        print_stacktrace(e)
        print("AssertionError occurred, indicating the presence of the issue.")
        os._exit(0)  # Exit with code 0 to indicate the issue was successfully reproduced
    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        os._exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script sets up a basic Django environment, including model definitions for `Product` and `Order`. The `reproduce_issue` function aims to reproduce the behavior described where an `Order` is saved after its related `Product` has had its non-auto `CharField` primary key specified but before the `Product` itself has been saved, leading to unexpected behaviors.

Here are the steps this script takes:
1. Configures Django with a minimal setup.
2. Defines the necessary models inline.
3. Attempts to reproduce the described issue within a transaction.
4. Uses the provided `print_stacktrace` function to clearly output any `AssertionError` resulting from the test, indicating the issue's presence.

Please note: This script should be run in an environment where Django is installed, using a command like `python3 reproducerer.py`.