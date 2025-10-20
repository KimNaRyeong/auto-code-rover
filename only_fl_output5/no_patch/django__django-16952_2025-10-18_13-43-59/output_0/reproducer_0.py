import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line

# Define settings for Django's standalone use
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()

# Models to reproduce the issue
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_pizza = models.BooleanField(default=False)

class ItalianRestaurant(Restaurant):
    serves_gnocchi = models.BooleanField(default=False)

class ItalianRestaurantManyParents(ItalianRestaurant, Place):
    pass

class Supplier(Place):
    customers = models.ManyToManyField(Restaurant, related_name="provider")

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

# Testing code
def test():
    try:
        ItalianRestaurantManyParents.objects.create(
            name="Ristorante Miron",
            address="1234 W. Ash",
        )
        print("Issue not reproduced - the object was created successfully.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present") from e

if __name__ == '__main__':
    # Initialize Django command line utilities
    argv = sys.argv[:1] + ['makemigrations', '__main__'] + sys.argv[1:]
    execute_from_command_line(argv)
    
    argv = sys.argv[:1] + ['migrate'] + sys.argv[1:]
    execute_from_command_line(argv)
    
    test()
