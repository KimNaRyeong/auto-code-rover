```python
import os
import django
from django.conf import settings
from django.db import models, transaction

# Configure Django for standalone script usage
def configure_django():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=('__main__',),
        USE_TZ=True,
    )
    django.setup()

# Define models
class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

# Function to print stack trace
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

def main():
    configure_django()
    from django.core.management import call_command
    call_command('makemigrations', '__main__', interactive=False)
    call_command('migrate', interactive=False)

    try:
        with transaction.atomic():
            order = Order()
            order.product = Product()
            order.product.sku = "foo"
            order.product.save()
            order.save()
            assert Order.objects.filter(product_id="").exists(), 'Product_id is not empty.'
            assert Order.objects.filter(product=order.product).exists(), 'Order with the specified product does not exist.'

        with transaction.atomic():
            order = Order()
            order.product = Product(sku="foo")
            order.product.save()
            order.save()
            assert Order.objects.filter(product=order.product).exists(), 'Order with the specified product does not exist.'
    except AssertionError as e:
        print_stacktrace(e)
        os._exit(1)
    else:
        print("No issue detected.")
        os._exit(0)

if __name__ == '__main__':
    main()
```

This `reproducer.py` script sets up a minimal Django environment, defines two models `Product` and `Order` with a ForeignKey relationship, and then attempts to reproduce the issue as described. 

Please ensure that you have Django installed in your environment where this script is going to be executed. If not, run `pip install django` to install Django.

If the issue exists as described, the script will catch an `AssertionError`, print a detailed stack trace with the `print_stacktrace` function, and exit with code 1 indicating the presence of the issue. If the issue does not occur, it will print "No issue detected." and exit with code 0, indicating that the issue is fixed.